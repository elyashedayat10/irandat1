from django import forms

from .models import Setting


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = (
            "title",
            "icon",
            "description",
        )
        labels = {
            "title": "عنوان",
            "icon": "ایکون",
            "description": "توضیحات",
        }

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "icon": forms.FileInput(attrs={"class": "form-control"}),
        }
