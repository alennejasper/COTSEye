from django.forms import ModelForm
from django.forms.widgets import FileInput
from django.contrib.auth.forms import UserCreationForm
from .models import User, Account


class AccountForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ["username", "password1", "password2"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number"]


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ["account", "date_joined"]
        widgets = {"profile_photo": FileInput()}