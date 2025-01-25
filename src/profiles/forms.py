
from django import forms

from profiles.models import UserProfiles

# Model form for update the user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        mmodel = UserProfiles
        fields = ('bio', 'city')
