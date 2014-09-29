from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from awards.models import *

def mail(entry):
    text_version = render_to_string('email/award_nomineealert.txt', {'entry': entry})
    linebreaked = text_version.replace('\n', '\n<br>')
    html_version = render_to_string('email/award_nomineealert.html', {'text': linebreaked})
    email = EmailMultiAlternatives(
        "You've been nominated!",
        text_version,
        '''"Jamie McGonnigal" <rootscamp@neworganizing.com>''',
        [entry.email]
    )
    email.attach_alternative(html_version, "text/html")
    email.send()

class Command(BaseCommand):
    """Email All The Nominees Who Have Not Been Emailed"""
    help = "Emails all the nominees who have not been emailed their edit location"

    def handle(self, *args, **options):
        mvo_nominees = MostValuableOrganizer.objects.filter(approved=True,contacted=False).exclude(email="").exclude(email__isnull=True)
        for nominee in mvo_nominees:
            mail(nominee)
            nominee.contacted = True
            nominee.save()
            self.stdout.write('Nominee: %s %s Code: %s Contacted: %s\n' % (nominee.name, nominee.email, nominee.secure_code(), nominee.contacted))

        mvt_nominees = MostValuableTechnology.objects.filter(approved=True,contacted=False).exclude(email="").exclude(email__isnull=True)
        for nominee in mvt_nominees:
            mail(nominee)
            nominee.contacted = True
            nominee.save()
            self.stdout.write('Nominee: %s %s Code: %s Contacted: %s\n' % (nominee.first_name, nominee.email, nominee.secure_code(), nominee.contacted))

        mvc_nominees = MostValuableCampaign.objects.filter(approved=True,contacted=False).exclude(email="").exclude(email__isnull=True)
        for nominee in mvc_nominees:
            mail(nominee)
            nominee.contacted = True
            nominee.save()
            self.stdout.write('Nominee: %s %s Code: %s Contacted: %s\n' % (nominee.first_name, nominee.email, nominee.secure_code(), nominee.contacted))
