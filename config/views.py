from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from .forms import SettingForm
from .models import Setting

# Create your views here.


class SettingCreateView( SuccessMessageMixin, CreateView):
    model = Setting
    success_message = "تنظیمات با موفقیت به روزرسانی شد"
    success_url = reverse_lazy("config:setting")
    form_class = SettingForm
    template_name = "config/create.html"


class SettingView( View):
    def get(self, request):
        setting = Setting.load()
        return render(request, "config/setting.html", {"setting": setting})


class PanelView(View):
    def get(self, request):
        return render(
            request,
            "config/panel.html",
        )
