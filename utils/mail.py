from django.template.loader import render_to_string
from django.urls import reverse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
#from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.template import Context


class TokenGenerator(PasswordResetTokenGenerator):
    pass


generate_token = TokenGenerator()


def send_mail(recipient, subject, body, user, url_name, **kwargs):
    domain = "http://188.132.130.99/"#Site.objects.get_current().domain
    try:
        _url_slug = reverse(url_name).split('/api/v1/auth')[1]
    except (IndexError, ValueError):
        _url_slug = reverse(url_name)

    domain = domain + _url_slug
    message = get_template('authentication/mail/user_activation.html').render({
        'body': body, 'user': user, 'url_name': url_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user), 'domain': domain,
        **kwargs})
    email = EmailMessage(subject, message, to=[recipient])
    try:
        email.content_subtype = "html"
        email.send()
    except Exception as e:
        print(e)


def send_password_reset_mail(recipient, user, url_name, **kwargs):
    domain = "http://188.132.130.99/" #Site.objects.get_current().domain
    subject = 'Password Reset'
    body = 'Please click the link below to reset your password'
    message = render_to_string('authentication/mail/password_reset.html',
                               {'body': body, 'user': user, 'url_name': url_name, 'domain': domain})
    email = EmailMessage(subject, message, to=[recipient])
    try:
        email.send()
    except Exception as e:
        print(e)
