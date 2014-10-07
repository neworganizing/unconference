from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib import messages

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
        # super(SubmitNominee, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if context['nomination_form'].is_valid() and \
                context['nominee_form'].is_valid() and \
                (request.user.is_authenticated() or
                 context['nominator_form'].is_valid()):
            if request.user.is_authenticated():
                user_profile = UserProfile.objects.get(user=request.user)
            else:
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

        if not self.request.user.is_authenticated():
            context['nominator_form'] = NominatorForm(
                data,
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


class UpdateAward(UpdateView):
    def get_object(self, queryset=None):
        super(UpdateAward, self).get_object(self.request, queryset=queryset)
        obj = get_object_or_404(
            self.model,
            slug=self.kwargs['slug'],
            unconference__slug=self.kwargs['unconference']
        )

        if obj.secure_code() != self.kwargs['code']:
            raise Http404

        return obj

    def get(self, request, *args, **kwargs):
        super(UpdateAward, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        context['update'] = True
        context['nominee'] = self.obj
        return self.render_to_response(context)


class UpdateMVO(UpdateView):
    model = MostValuableOrganizer
    form_class = MostValuableOrganizerSubmissionForm
    template_name = "awards/display_mvo.html"


class UpdateMVC(UpdateView):
    model = MostValuableCampaign
    template_name = "awards/display_mvc.html"


class UpdateMVT(UpdateView):
    model = MostValuableTechnology
    template_name = "awards/display_mvt.html"


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

    context['unconference'] = Unconference.objects.get(slug=unconference)
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
