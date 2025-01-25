from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfiles

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Creation of the profile if the user is newly created
    if created:
        UserProfiles.objects.create(user=instance)
    # Save existing profile only if it is linked to the user
    elif hasattr(instance, 'profile'):
        instance.profile.save()
