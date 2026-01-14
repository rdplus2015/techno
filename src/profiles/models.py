from django.conf import settings
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    # Link the profil to the use
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return  f'profile of {self.user.pseudonym}'