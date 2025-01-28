
from django.urls import path

from profiles.views import UserProfileView, UserProfileUpdate

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdate.as_view(), name='profileUpdate'),
]

