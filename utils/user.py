from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from authentication.models import User
from utils.mail import generate_token


class UserMailActivation:
    @staticmethod
    def validate_token(uidb64, token):
        validation = False
        user = None
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            pass

        if user is not None and generate_token.check_token(user, token):
            validation = True
            if not user.activation:
                user.activation = True
                user.save()

        return user if user and validation else None