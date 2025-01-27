# Auth urls

from django.urls import path

from accounts.views import UserSignupView, UserLoginView, UserLogoutView, UserUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
   # Authentification urls and password reset
   path('signup/', UserSignupView.as_view(), name='signup'),
   path('login/', UserLoginView.as_view(), name='login'),
   path('logout/', UserLogoutView.as_view(), name='logout'),

   path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

   # User informations Update
   path('profile/security/update/password/', auth_views.PasswordChangeView.as_view(template_name='profile/security/update_user_password.html'), name='update_user_password'),
   path('profile/security/update/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='profile/security/update_user_password_done.html'), name='password_change_done'),
   path('profile/security/update/user',  UserUpdateView.as_view(), name='userUpdate'),
]

