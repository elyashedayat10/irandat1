from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import ValidationError

from .models import User


class CreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone_number",)

    def clean(self):
        clean_data = super(CreationForm, self).clean()
        password, password_confirm = (
            clean_data["password"],
            clean_data["password_confirm"],
        )
        if (password and password_confirm) and (password != password_confirm):
            raise ValidationError("un match password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("phone_number",)
