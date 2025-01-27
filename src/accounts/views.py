from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView

from accounts.forms import SignUpForm, UserUpdateForm


# Create your views here.

# Sign-up view for handling user registration
class UserSignupView(View):
    # Specifies the template to be used for rendering the sign-up page.
    template_name = 'registration/signup.html'

    # Handles GET requests to display the sign-up form.
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url()) # Redirect authenticated users
        form = SignUpForm() # Initialize a new sign-up form
        return render(request, self.template_name, {'form':form}) # Render the sign-up form

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())  # Redirect authenticated users
        form = SignUpForm(request.POST) # Bind the form with POST data
        if form.is_valid():
            user = form.save() # Save the new user
            login(request, user) # Log in the new user
            return redirect(self.get_success_url())  # Redirect to the success URL
        return render(request, self.template_name, {'form':form}) # Re-render the form with errors

    def get_success_url(self):
        """Return the URL to redirect to after successful sign-up."""
        next_url = self.request.GET.get('next')  # Get the 'next' parameter
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url  # Redirect to the 'next' URL if it's safe
        return reverse('index')  # Default redirect to the dashboard

    def get_redirect_url(self):
        """Return the URL to redirect authenticated users."""
        return reverse('index')  # Redirect to the dashboard

# Custom login view that redirects authenticated users to the Blog index page
class UserLoginView(LoginView):
    template_name = 'registration/login.html' # Template for the login page
    redirect_authenticated_user = True # Redirect already logged-in users

    def get_success_url(self):
        next_url = self.request.GET.get('next') # Get the 'next' parameter from the template
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url # Redirect to the 'next' URL if it's safe
        return  reverse('index') # redirect to the Blog index page

# Custom and secure logoutView
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index') # Default URL to redirect to after logout

    def post(self, request, *args, **kwargs):
        next_url = request.POST.get('next') # Get the 'next' URL from the POST request
        if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
            self.next_page = next_url  # Set next_page to the safe 'next' URL
        return super().post(request, *args, **kwargs) # Call the parent method

    def get(self, request, *args, **kwargs):
        return  HttpResponseNotAllowed(['POST']) # Only allow POST requests for logout

# Custom view for update user information, restricted to logged-in users
class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'profile/security/updateUser.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return  self.request.user


class