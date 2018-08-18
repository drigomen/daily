from django.contrib.auth import forms
from .models import User


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        # fields = forms.UserCreationForm.Meta.fields + ('custom_field', )
