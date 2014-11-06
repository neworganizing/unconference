from celery import task
from .models import (MostValuableOrganizer, MostValuableCampaign,
                     MostValuableTechnology)
from django.utils.translation import ugettext_lazy as _

from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.core.signing import Signer


@task
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
    for mvo_nominee in pending_mvo_nominees:
        to = mvo_nominee.profile.user.email
        token = signer.sign(mvo_nominee.profile.user.pk)

        print token

        html = render_to_string(
            "awards/emails/mvo_nominee_email.html",
            {
                "nominee": mvo_nominee,
                "token": token
            }
        )
        text = strip_tags(html)

        msg = EmailMultiAlternatives(subject, text, from_email, [to])
        msg.attach_alternative(html, "text/html")
#        msg.send()

#        mvo_nominee.contacted = True
#        mvo_nominee.save()
