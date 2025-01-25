from django.views.generic import DetailView

from profiles.models import UserProfiles


# Create your views here.


class ProfilesView(DetailView):
    model = UserProfiles
    template_name = 'profile/profileView.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Get the profile for the currently logged-in user
        user = self.request.user.id
        profile = UserProfiles.objects.get(user_id=user) # Retrieve the profile based on user ID
        return profile
