from django import forms
from .models import Posts

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            "title",
            "description",
            "content",
            "image",
            "category",
            "status",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 8}),
            "categories": forms.CheckboxSelectMultiple(),  #  SelectMultiple
        }
