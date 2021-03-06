from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.core.signing import Signer

from thewall.models import Unconference

from awards.models import (MostValuableOrganizer, MostValuableTechnology,
                           MostValuableCampaign)
from awards.forms import (MostValuableOrganizerSubmissionForm,
                          MostValuableTechnologySubmissionForm,
                          MostValuableCampaignSubmissionForm,
                          MostValuableOrganizerEditForm,
                          MostValuableTechnologyEditForm,
                          MostValuableCampaignEditForm,
                          NominatorForm,
                          NomineeForm)
from awards.utils import award_to_actionkit, render_to, get_user_profile_model

UserProfile = get_user_profile_model()


class SubmitNominee(TemplateView):
    template_name = "awards/submit_nominee.html"
    form_class = None
    award = None
    akit_page = None
    unconference = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # if the user does not yet have a profile, they should have
        # seen the nominator form and filled it out
        user_profile = None
        if request.user.is_authenticated():
            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                pass

        if context['nomination_form'].is_valid() and \
                context['nominee_form'].is_valid() and \
                (user_profile or
                 context['nominator_form'].is_valid()):

            # Save the user's profile if they didn't already have one
            if not user_profile:
                user_profile = context['nominator_form'].save()

            nominee = context['nominee_form'].save()
            nomination = context['nomination_form'].save(commit=False)
            nomination.nominator = user_profile
            nomination.profile = nominee

            try:
                nomination.organization = nominee.organization
            except:
                pass

            nomination.save()

            messages.success(
                request,
                """
                Thanks for submitting your nomination!  It will
                become visible on this page once the nominee has
                confirmed the submission.
                """
            )

            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(
                request,
                "There was a problem with your nomination!"
            )
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SubmitNominee, self).get_context_data(**kwargs)
        context['unconference'] = get_object_or_404(
            Unconference, slug=kwargs['unconference']
        )
        self.unconference = context['unconference']

        context['award'] = kwargs['award']

        if kwargs['award'] == "mvo":
            self.form_class = MostValuableOrganizerSubmissionForm
            self.award = "MVO"
            self.akit_page = "RC_2014_MVOnominees"
        elif kwargs['award'] == "mvt":
            self.form_class = MostValuableTechnologySubmissionForm
            self.award = "MVT"
            self.akit_page = "RC_2014_MVTnominees"
        elif kwargs['award'] == "mvc":
            self.form_class = MostValuableCampaignSubmissionForm
            self.award = "MVC"
            self.akit_page = "RC_2014_MVCnominees"

        if self.request.POST:
            data = self.request.POST
        else:
            data = None

        context['nomination_form'] = self.form_class(
            data,
            initial={
                'unconference': context['unconference']
            },
            prefix="nomination"
        )

        # If logged in, determine if the user has a profile
        if self.request.user.is_authenticated():
            try:
                context['user_profile'] = UserProfile.objects.get(
                    user=self.request.user
                )
            except:
                context['user_profile'] = None
        else:
            context['user_profile'] = None

        # If no profile existed, initialize or populate
        # the nominator form
        if not context['user_profile']:
            if self.request.user.is_authenticated() and not data:
                initial = {
                    'email': self.request.user.email,
                    'first_name': self.request.user.first_name,
                    'last_name': self.request.user.last_name
                }
            else:
                initial = None

            context['nominator_form'] = NominatorForm(
                data,
                initial=initial,
                prefix='nominator'
            )

        context['nominee_form'] = NomineeForm(
            data,
            prefix='nominee'
        )

        return context

    def form_valid(self, form):
        # Send post to actionkit
        import logging
        ak_logger = logging.getLogger('actionkit')

        try:
            award_to_actionkit(self.akit_page, self.award, form.cleaned_data)
        except Exception, e:
            ak_logger.error(unicode(e))

        # Save the submission
        form.save(commit=True)
        return super(SubmitNominee, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "list_award_nominees",
            kwargs={"unconference": self.unconference.slug}
        )


class UpdateNominee(UpdateView):
    template_name = "awards/update_nominee.html"

    def get_object(self, queryset=None):
        # super(UpdateNominee, self).get_object(queryset=queryset)

        try:
            self.object = self.model.objects.get(
                slug=self.kwargs['slug'],
                unconference__slug=self.kwargs['unconference']
            )
        except self.model.DoesNotExist:
            print "Nominee not found!"
            return Http404
        except self.model.MultipleObjectsReturned:
            matches = self.model.objects.filter(
                slug=self.kwargs['slug'],
                unconference__slug=self.kwargs['unconference']
            ).order_by('created_at')
            self.object = matches[0]

        return self.object

    def get(self, request, *args, **kwargs):
        self.configure_award(**kwargs)

        # Ensure proper token has been passed
        token = request.GET.get('token', None)

        if not token:
            return HttpResponseRedirect(
                reverse(
                    'list_award_nominees',
                    kwargs={
                        "unconference": kwargs['unconference']
                    }
                )
            )

        super(UpdateNominee, self).get(request, *args, **kwargs)

        context = self.get_context_data(**kwargs)
        context['nominee'] = self.object
        context['form'] = self.form(instance=self.object)

        signer = Signer()
        user_id = signer.unsign(token)

        if int(user_id) != int(self.object.profile.user.pk):
            print "User id from token: ",  user_id
            print "User id from db: ", self.object.profile.user.pk
            return HttpResponseRedirect(
                reverse(
                    'list_award_nominees',
                    kwargs={
                        "unconference": kwargs['unconference']
                    }
                )
            )

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.configure_award(**kwargs)

        form = self.form(
            request.POST, request.FILES, instance=self.get_object()
        )

        print form

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'list_award_nominees',
                    kwargs={'unconference': kwargs['unconference']}
                )
            )

        context = self.get_context_data(**kwargs)
        context['nominee'] = self.object
        context['form'] = form

        return self.render_to_response(context)

    def configure_award(self, **kwargs):
        if kwargs['award'] == 'mvo':
            self.model = MostValuableOrganizer
            self.form = MostValuableOrganizerEditForm
        elif kwargs['award'] == 'mvc':
            self.model = MostValuableCampaign
            self.form = MostValuableCampaignEditForm
        elif kwargs['award'] == 'mvt':
            self.model = MostValuableTechnology
            self.form = MostValuableTechnologyEditForm
        else:
            raise Exception


def nominee_update_award_form(request, unconference, award, slug):
    # Make sure there is a secure code in the URL
    if 'code' not in request.GET:
        raise Http404

    if award == 'mvo':
        model = MostValuableOrganizer
        form = MostValuableOrganizerEditForm
        template = "awards/display_mvo.html"
    elif award == 'mvc':
        model = MostValuableCampaign
        form = MostValuableCampaignEditForm
        template = "awards/display_mvc.html"
    elif award == 'mvt':
        model = MostValuableTechnology
        form = MostValuableTechnologyEditForm
        template = "awards/display_mvt.html"
    else:
        raise Http404

    # Request the object
    if request.user.is_authenticated():
        nom = get_object_or_404(
            model, slug=slug, unconference__slug=unconference
        )
    else:
        nom = get_object_or_404(
            model, slug=slug, unconference__slug=unconference
        )

    # Confirm that the secure code is correct
    if nom.secure_code() != request.GET['code']:
        raise Http404

    editform = form(instance=nom)
    context = {'nominee': nom, 'form': editform}
    return render(request, template, context)


def nominee_update_award(request):
    if request.method == 'GET':
        raise Http404

    award = request.POST['award']
    if award == 'mvo':
        model = MostValuableOrganizer
    elif award == 'mvc':
        model = MostValuableCampaign
    elif award == 'mvt':
        model = MostValuableTechnology
    else:
        raise Http404

    obj = get_object_or_404(model, pk=request.POST['id'])
    if obj.secure_code() != request.POST['secure_code']:
        print "Bad Code!"
        raise Http404

    if 'image' in request.FILES:
        obj.image = request.FILES['image']
    if 'personal_statement' in request.POST:
        obj.personal_statement = request.POST['personal_statement']
    if 'twitter' in request.POST:
        obj.twitter = request.POST['twitter']

    obj.save()
    return redirect(request.POST['redirect'])


@render_to("awards/list_all_nominees.html")
def list_award_nominees(request, unconference, award=None):
    context = dict()

    context['nominees'] = []

    if award == 'mvo' or not award:
        nominee_data = {
            "object_list": MostValuableOrganizer.objects.select_related(
                'unconference'
            ).filter(
                unconference__slug=unconference, approved=True
            ).order_by('profile__user__first_name'),
            "short_award_name": "mvo",
            "long_award_name": "Most Valuable Organizer"
        }
        context['nominees'].append(nominee_data)

    if award == 'mvt' or not award:
        nominee_data = {
            "object_list": MostValuableTechnology.objects.select_related(
                'unconference'
            ).filter(
                unconference__slug=unconference, approved=True
            ).order_by('profile__user__first_name'),
            "short_award_name": "mvt",
            "long_award_name": "Most Valuable Technology"
        }
        context['nominees'].append(nominee_data)

    if award == 'mvc' or not award:
        nominee_data = {
            "object_list": MostValuableCampaign.objects.select_related(
                'unconference'
            ).filter(
                unconference__slug=unconference, approved=True
            ).order_by('profile__user__first_name'),
            "short_award_name": "mvc",
            "long_award_name": "Most Valuable Campaign"
        }
        context['nominees'].append(nominee_data)

    try:
        context['unconference'] = Unconference.objects.get(slug=unconference)
    except:
        raise Http404

    return context


class DisplayNominee(TemplateView):
    def get(self, request, *args, **kwargs):
        self.award = kwargs['award']
        context = self.get_context_data(*args, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(DisplayNominee, self).get_context_data(*args, **kwargs)

        context['unconference'] = Unconference.objects.get(
            slug=kwargs['unconference']
        )

        if self.request.user.is_authenticated():
            query = {
                "slug": kwargs['slug'],
                "unconference__slug": context['unconference'].slug
            }
        else:
            query = {
                "slug": kwargs['slug'],
                "unconference__slug": context['unconference'].slug,
                "approved": True
            }

        if self.award == 'mvo':
            context['nominee'] = get_object_or_404(
                MostValuableOrganizer,
                **query
            )
        elif self.award == 'mvt':
            context['nominee'] = get_object_or_404(
                MostValuableTechnology,
                **query
            )
        elif self.award == 'mvc':
            context['nominee'] = get_object_or_404(
                MostValuableCampaign,
                **query
            )

        return context

    def get_template_names(self):
        return ['awards/display_'+self.award+'.html']
