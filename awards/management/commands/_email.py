from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send(me,you,msg,SERVER,USER,PASS):
    import smtplib
    s = smtplib.SMTP(SERVER)
    s.starttls()
    s.login(USER,PASS)
    s.sendmail(me,you,msg)

def md5hex(text,seed=''):
    import md5
    return md5.md5('%s%s' % (text,seed)).hexdigest()

me = 'award@neworganizing.com'
you = 'nickcatalano@neworganizing.com'

seed = 'NOINOInoinoi'
urlhash = md5hex(you,seed)[0:6]

url = "http://rootscamp.neworganizing.com/awards/edit/123123?conf=%s" % urlhash

msg = MIMEMultipart('alternative')
msg['Subject'] = "You've been nominated for an award"
msg['From'] = '"Jamie McGonnigal, NOI" <award@neworganizing.com>'
msg['To'] = '"Nick Catalano" <nickcatalano@neworganizing.com>'

text = "Hi Nick\nHow are you?\nHere's the link you wanted\n\nJust visit %s to claim your prize" % url
html = '''
<html><body>Hi Nick,<br><br>Guess what? You've been nominated for a MVO Award!<br><br>
Just visit <a href="%s">%s</a> to claim your prize<br><br>
Sincerely,<br><br>
NOI Staff</body></html>
''' % (url, url)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer():
    """A general SMTP mailer"""
    def __init__(self, server,user,password):
        super(Mailer, self).__init__()
        self.server = server
        self.user = user
        self.password = password

    def mailer(msg):
        pass

    def send():
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        msg = MIMEMultipart('alternative')

        if self.subject:
            msg['Subject'] = self.subject
        else:
            msg['Subject'] = 'No Subject'

        if self.friendly_to:
            msg['']

        # Attach our text message
        msg.attach(MIMEText('text',self.text))

        # Detect if there is HTML
        if self.html:
            msg.attach(MIMEText('html',self.html)

        _mailer(msg)
        
        

part1 = MIMEText(text,'plain')
part2 = MIMEText(html,'html')

msg.attach(part1)
msg.attach(part2)

send(me,you,msg.as_string(),SERVER,USER,PASS)

s = smtplib.SMTP(SERVER)
s.starttls()
s.login(USER,PASS)
s.sendmail(me,you,msg)

from django.template import Context, Template

t = Template(message)
c = Context()

def send_mail_template(subject, template, addr_from, addr_to, context=None,
    attachments=None, fail_silently=False):
    """
    Send email rendering text and html versions for the specified template name
    using the context dictionary passed in. Arguments are as per django's 
    send_mail apart from template which should be the common path and name of 
    the text and html templates without the extension, for example:
    "email_templates/contact" where both "email_templates/contact.txt" and 
    "email_templates/contact.html" exist.
    """
    from django.core.mail import EmailMultiAlternatives
    from django.template import loader, Context
    if context is None:
        context = {}
    if attachments is None:
        attachments = []
    # allow for a single address to be passed in
    if not hasattr(addr_to, "__iter__"):
        addr_to = [addr_to]
    # loads a template passing in vars as context
    render = lambda type: loader.get_template("%s.%s" % 
        (template, type)).render(Context(context))
    # create and send email
    msg = EmailMultiAlternatives(subject, render("txt"), addr_from, addr_to)
    msg.attach_alternative(render("html"), "text/html")
    for attachment in attachments:
        msg.attach(attachment)
    msg.send(fail_silently=fail_silently)