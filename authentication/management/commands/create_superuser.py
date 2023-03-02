from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        email = "idcp@idcp.com"
        try:
            User.objects.get(email=email)
            return
        except User.DoesNotExist:
            pass
        if User.objects.count() == 0:

            admin = User.objects.create_superuser(username=email, email=email, password="12345@!")
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Zaten bir admin hesabı olduğu için eklenmedi')

