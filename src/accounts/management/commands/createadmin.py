from django.core.management.base import BaseCommand
from accounts.models import TechnoUser
import os


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        email = os.environ.get('ADMIN_EMAIL', 'a@a.com')
        password = os.environ.get('ADMIN_PASSWORD', 'TechnoAdmin123!')

        u, created = TechnoUser.objects.get_or_create(email=email)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.save()

        if created:
            self.stdout.write(f'Superuser created: {email}')
        else:
            self.stdout.write(f'Superuser updated: {email}')



            