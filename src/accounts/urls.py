# Auth urls

from django.urls import path

from .views import SignUp

urlpatterns = [
   path('signup/', SignUp.as_view(template_name='registration/signUp.html'), name='signup'),
]
