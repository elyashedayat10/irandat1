from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

from .models import LegalArticle


class LegalArticleForm(forms.ModelForm):
    class Meta:
        model = LegalArticle
        fields = (
            "number",
            "description",
            "approved",
        )
        labels = {
            "number": "شماره ماده",
            "description": "توضیحات ",
            "approved": "تاریخ ثبت",
        }
        widgets = {
            "number": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(LegalArticleForm, self).__init__(*args, **kwargs)
        self.fields["approved"] = JalaliDateField(
            label="تاریخ ثبت", widget=AdminJalaliDateWidget
        )
