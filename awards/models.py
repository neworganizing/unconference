from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from autoslug import AutoSlugField

from thewall.models import Unconference
from utils import get_user_profile_model_name, get_organization_model_name

# UserProfile = get_user_profile_model()
# Organization = get_organization_model()


class AwardNominee(models.Model):
    unconference = models.ForeignKey(
        Unconference, verbose_name="Related Unconference",
        help_text="Which RootsCamp is this nomination for"
    )

    nominator = models.ForeignKey(
        get_user_profile_model_name(), related_name="%(class)s_nominees"
    )

    profile = models.ForeignKey(
        get_user_profile_model_name(), related_name="%(class)s_nominations"
    )

    """
    Fields now located on UserProfile

    nominator_first_name = models.CharField(
        verbose_name="Your First Name",
        null=False, blank=False, max_length=15
    )
    nominator_last_name = models.CharField(verbose_name="Your Last Name",
        null=False, blank=False, max_length=50)
    nominator_email = models.EmailField(verbose_name="Your email address",
        null=False, blank=False, validators=[validate_email])
    nominator_zip = models.IntegerField(verbose_name="Your zip code",
        blank=False)
    nominator_twitter_handle = models.CharField(
        verbose_name="Your twitter handle",
        help_text="Don't include the @", null=True, blank=True, max_length=50)
    image = models.ImageField(
        verbose_name="Picture of Nominee",
        upload_to="awardnominees", null=True, blank=True,
        width_field='width,
        height_field='height'
    )
    width = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True, blank=True)
    """

    relationship = models.CharField(
        verbose_name="Relationship to nominee",
        help_text="How do you know the nominee?",
        null=False, blank=False, max_length=50
    )

    approved = models.BooleanField(
        verbose_name="Approved",
        help_text="Can this be displayed on the website",
        default=False
    )

    contacted = models.BooleanField(
        verbose_name="Emailed with Confirmation Code", default=False
    )

    personal_statement = models.TextField(
        verbose_name="Nominee Personal Statement",
        blank=True, null=True
    )

    class Meta:
        verbose_name = _('Award Nominee')
        verbose_name_plural = _('Award Nominees')
        abstract = True

    def get_absolute_url(self):
        return reverse('display_nominee', kwargs={
            "unconference": self.unconference.slug,
            "award": self.short_name,
            "slug": self.slug
        })

    def secure_code(self):
        import md5
        return md5.md5(str(self.id)+settings.SECRET_KEY).hexdigest()[0:6]

    def edit_url(self):
        return """
            /awards/%s/%s/edit/%s/?code=%s
        """ % (
            self.unconference.slug, self.short_name,
            self.slug, self.secure_code()
        )

    def email_to(self):
        if self.short_name in ['mvc', 'mvt']:
            return self.first_name
        else:
            return self.name()

    def email_what(self):
        if self.short_name == 'mvo':
            return 'you'
        else:
            return self.name()

    def __unicode__(self):
        return "Nomination by %s %s" % (
            self.nominator.first_name, self.nominator.last_name
        )


# Most Valuable Organizer Model
class MostValuableOrganizer(AwardNominee):
    slug = AutoSlugField(populate_from='profile', unique_with='unconference')

    """
    name = models.CharField(
        verbose_name="Nominee's Name", blank=False, null=False, max_length=50
    )
    twitter = models.CharField(
        verbose_name="Nominee's Twitter Handle", max_length=50,blank=True
    )
    email = models.EmailField(
        verbose_name="Nominee's Email Address", blank=False, null=False,
        validators=[validate_email]
    )
    phone_number = models.CharField(
        verbose_name="Nominee's Phone Number",max_length=15,blank=True
    )
    organization = models.CharField(
        verbose_name="Nominee's Organization",max_length=50,blank=True
    )
    org_website = models.URLField(
        verbose_name="Organization Website",blank=True,
        validators=[URLValidator]
    )
    """

    innovation = models.TextField(
        verbose_name="Innovation", blank=False,
        help_text="""
            Did the nominee think "outside the box"?
            Give an example of an innovative response to a challenge
        """
    )
    respect = models.TextField(
        verbose_name="Respect", blank=False,
        help_text="""
            Describe a way in which the nominee developed a
            culture of respect within the campaign
        """
    )
    courage = models.TextField(
        verbose_name="Courage", blank=False,
        help_text="""
            Did the nominee take real risks when necessary?
            Describe a specific example, and tell us the outcome
            of taking the risk
        """
    )
    excellence = models.TextField(
        verbose_name="Excellence", blank=False,
        help_text="""
            How did the nominee model an expectation of excellence?
            Did the nominee inspire others to excellence?
        """
    )
    comments = models.TextField(
        verbose_name="Additional Comments", blank=True,
        help_text="""Is there anything else we should know when
            considering this nominee?
        """
    )

    short_name = "mvo"
    long_award_name = "Most Valuable Organizer"

    class Meta:
        verbose_name = _('Most Valuable Organizer')
        verbose_name_plural = _('Most Valuable Organizers')

    def __unicode__(self):
        return '%s of %s for Most Valuable Organizer' % (
            self.name, self.profile.organization
        )

    @property
    def name(self):
        return u"{0} {1}".format(
            self.profile.first_name, self.profile.last_name
        )

    @property
    def image(self):
        return self.profile.photo

    @property
    def twitter(self):
        return self.profile.twitter_handle


# Most Valuable Technology Model
class MostValuableTechnology(AwardNominee):
    name = models.CharField(
        verbose_name="Technology Nominated", max_length=50,
        blank=False, null=False
    )

    slug = AutoSlugField(populate_from='name', unique_with='unconference')

    organization = models.ForeignKey(
        get_organization_model_name(),
        related_name="mvt_nominations"
    )

    """
    first_name = models.CharField(
        verbose_name="Director's First Name", max_length=50,blank=True)
    last_name = models.CharField(
        verbose_name="Director's Last Name", max_length=50,blank=True)
    email = models.EmailField(
        verbose_name="Director's Email",blank=True,
        validators=[validate_email])
    organization_website = models.URLField(
        verbose_name="Company Website",blank=False, validators=[URLValidator])
    organization = models.CharField(
        verbose_name="Company Twitter Handle", max_length=50,blank=True)
    """

    innovation = models.TextField(
        verbose_name="Innovation", blank=False,
        help_text="""
            What challenge does this tech provide a solution for?
            How did it creatively address a problem?
        """
    )

    potential = models.TextField(
        verbose_name="Potential", blank=False,
        help_text="""How does this change the game?
            What new possibilities does it provide?
        """
    )

    accessibility = models.TextField(
        verbose_name="Accessibility", blank=False,
        help_text="""How accessible was the tech?
            Tell us about the ease of use, cost, and other ways
            that it was accessible to a broad spectrum.
        """
    )

    additional = models.TextField(
        verbose_name="Additional Info", blank=True,
        help_text="""
            Is there anything else we should know
            when considering this nominee?
        """
    )

    short_name = "mvt"
    long_award_name = "Most Valuable Technology"

    class Meta:
        verbose_name = _('Most Valuable Technology')
        verbose_name_plural = _('Most Valuable Technologies')

    def __unicode__(self):
        return '%s for Most Valuable Technology' % self.name

    @property
    def image(self):
        return self.organization.logo

    @property
    def twitter(self):
        return self.organization.twitter


# Most Valuable Organizer Model
class MostValuableCampaign(AwardNominee):
    name = models.TextField(
        verbose_name="Campaign/Organization Name",
        blank=False, null=False, max_length=50
    )

    slug = AutoSlugField(populate_from='name', unique_with='unconference')

    organization = models.ForeignKey(
        get_organization_model_name(),
        related_name="mvc_nominations"
    )

    """
    first_name = models.CharField(
        verbose_name="Campaign Manager's First Name",max_length=50,blank=True)
    last_name = models.CharField(
        verbose_name="Campaign Manager's Last Name",max_length=50,blank=True)
    email = models.EmailField(
        verbose_name="Campaign Manager's Email",blank=True,
        validators=[validate_email])
    website = models.URLField(
        verbose_name="Campaign Website",blank=True,
        validators=[URLValidator])
    twitter = models.CharField(
        verbose_name="Nominee's Twitter Handle", max_length=50,blank=True)
    """

    innovation = models.TextField(
        verbose_name="What innovative approaches did the campaign take?",
        blank=False, help_text="""
            What challenges did the campaign face?
            How did they respond/adapt?
        """)
    change = models.TextField(
        verbose_name="What change did this campaign hope to create?",
        blank=False, help_text="""
            Tell us what the campaign set out to achieve,
            and if they achieved it
        """
    )
    motivate = models.TextField(
        verbose_name="How did the campaign motivate you to participate?",
        blank=False, help_text="""
            What was the vision? How did they engage you and make
            you feel valuable?
        """
    )
    creative = models.TextField(
        verbose_name="What was creative or different about this campaign?",
        blank=False, help_text="""
            Did they try new tactics? Develop engaging strategies?
            How did they set themselves apart?
        """
    )
    additional = models.TextField(
        verbose_name="Additional Comments",
        help_text="What else makes this the Most Valuable Campaign?",
        blank=True
    )

    short_name = "mvc"
    long_award_name = "Most Valuable Campaign"

    class Meta:
        verbose_name = _('Most Valuable Campaign')
        verbose_name_plural = _('Most Valuable Campaigns')

    def __unicode__(self):
        return '%s for Most Valuable Campaign' % self.name

    @property
    def image(self):
        return self.organization.logo

    @property
    def twitter(self):
        return self.organization.twitter
