from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Custom mixin that extends Django's LoginRequiredMixin
class TechnoLoginRequiredMixin(LoginRequiredMixin):
    login_url = settings.LOGIN_URL  # URL to redirect to if the user is not logged in
    redirect_field_name = 'next'  # Name of the GET parameter to redirect to after login

    # Custom method to handle cases where the user does not have permission
    def handle_no_permission(self):
        from django.contrib import messages
        # Add a message to inform the user they need to be logged in
        messages.add_message(self.request, messages.INFO, 'You need to be logged in to view this page.')
        return super().handle_no_permission()




