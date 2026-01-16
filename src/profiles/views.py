from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from profiles.models import UserProfile
from techno.mixims import TechnoLoginRequiredMixin


# Create your views here.

# View to display user profile details
class UserProfileView(DetailView, TechnoLoginRequiredMixin):
    model = UserProfile
    template_name = 'profile/profileView.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Get the profile for the currently logged-in user
        user = self.request.user.id
        profile = UserProfile.objects.get(user_id=user) # Retrieve the profile based on user ID
        return profile

# View to update user profile details
class UserProfileUpdate(UpdateView, TechnoLoginRequiredMixin):
    model = UserProfile
    fields = ['bio', 'city', 'name']
    template_name = 'profile/ProfileUpdate.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return  UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        # Ensure that the profile being updated belongs to the current user
        if form.instance.user != self.request.user:
            return redirect('profile')  # Redirect if the profile does not belong to the current user
        return super().form_valid(form)  # Proceed with the form submission if the user is valid
