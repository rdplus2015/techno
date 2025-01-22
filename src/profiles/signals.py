from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profiles

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)
    else:
        instance.profile.save()  # If the user already exists and is updated, the profile is saved
        # The related name profile corresponds to the related_name you used in the OneToOneField in the Profiles model.