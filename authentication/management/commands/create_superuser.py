from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
            email = "idcp@idcp.com"
            admin = User.objects.create_superuser(username=email, email=email, password="12345@!")
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Zaten bir admin hesabı olduğu için eklenmedi')

