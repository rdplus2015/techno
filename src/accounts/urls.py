# Auth urls

from django.urls import path

from accounts.views import UserSignupView, UserLoginView, UserLogoutView

urlpatterns = [
   path('signup/', UserSignupView.as_view(template_name='registration/signup.html'), name='signup'),
   path('login/', UserLoginView.as_view(template_name='registration/login.html'), name='login'),
   path('logout/', UserLogoutView.as_view(), name='logout'),
]
