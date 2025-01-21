from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.urls import reverse_lazy, reverse

from src.accounts.forms import SignUpForm


# Create your views here.

class SignUp(View):
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
