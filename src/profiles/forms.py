
from django import forms

from profiles.models import UserProfile

# Model form for update the user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        mmodel = UserProfile
        fields = ('bio', 'city', 'name')
