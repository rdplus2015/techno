from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class SignUpForm(UserCreationForm):
    # Adding fields explicitly here for validations
    email = forms.EmailField(required=True)
    pseudonym = forms.CharField(max_length=12)

    class Meta:
        model = get_user_model()  # Telling Django to use TechnoUser model for the fields
        fields = ('pseudonym', 'email', 'password1', 'password2')  # Defining the fields to be included in the form

    def save(self, commit=True):
        user = super().save(commit=False)  # Calling the parent class's save method with commit=False to get a user instance without saving it to the database yet.
        user.email = self.cleaned_data['email']  # Setting the email field of the user instance to the cleaned data from the form.
        pseudonym = self.cleaned_data['pseudonym']

        if pseudonym.isalnum():
            user.pseudonym = pseudonym
        else:
            raise forms.ValidationError("The pseudonym must contain only letters and numbers.")

        # If commit is True, save the user instance to the database.
        if commit:
            user.save()
        # Returning the user instance.
        return user

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'pseudonym',)
