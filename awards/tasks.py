from celery import task
from .models import (MostValuableOrganizer, MostValuableCampaign,
                     MostValuableTechnology)
from django.utils.translation import ugettext_lazy as _

from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.signing import Signer
from django.conf import settings

from django.contrib.sites.models import Site


@task(name="awards.send_nominee_emails")
def send_nominee_emails():
    pending_mvo_nominees = MostValuableOrganizer.objects.filter(
        contacted=False,
        approved=True
    )
    pending_mvc_nominees = MostValuableCampaign.objects.filter(
        contacted=False,
        approved=True
    )
    pending_mvt_nominees = MostValuableTechnology.objects.filter(
        contacted=False,
        approved=True
    )

    signer = Signer()
    from_email = 'NOI <info@neworganizing.com>'
    subject = _(u"You've been nominated for an award!")
    current_site = Site.objects.get(pk=settings.SITE_ID)

    for mvo_nominee in pending_mvo_nominees:
        to = mvo_nominee.profile.user.email
        token = signer.sign(mvo_nominee.profile.user.pk)

        print token

        html = render_to_string(
            "awards/emails/mvo_nominee_email.html",
            {
                "nominee": mvo_nominee,
                "token": token,
                "domain": current_site.domain
            }
        )
        text = strip_tags(html)

        msg = EmailMultiAlternatives(subject, text, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()

        mvo_nominee.contacted = True
        mvo_nominee.save()

    for mvc_nominee in pending_mvc_nominees:
        to = mvc_nominee.profile.user.email
        token = signer.sign(mvc_nominee.profile.user.pk)

        print token

        html = render_to_string(
            "awards/emails/mvc_nominee_email.html",
            {
                "nominee": mvc_nominee,
                "token": token,
                "domain": current_site.domain
            }
        )
        text = strip_tags(html)

        msg = EmailMultiAlternatives(subject, text, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()

        mvc_nominee.contacted = True
        mvc_nominee.save()

    for mvt_nominee in pending_mvt_nominees:
        to = mvt_nominee.profile.user.email
        token = signer.sign(mvt_nominee.profile.user.pk)

        print token

        html = render_to_string(
            "awards/emails/mvt_nominee_email.html",
            {
                "nominee": mvt_nominee,
                "token": token,
                "domain": current_site.domain
            }
        )
        text = strip_tags(html)

        msg = EmailMultiAlternatives(subject, text, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()

        mvt_nominee.contacted = True
        mvt_nominee.save()
