
from django.urls import path

from profiles.views import ProfilesView

urlpatterns = [
    path('profile/', ProfilesView.as_view(template_name='profile/profileView.html'), name='profile')
]

