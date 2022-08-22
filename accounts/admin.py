from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin

from .forms import ChangeForm, CreationForm
from .models import OtpCode, User

admin.site.register(OtpCode)


# Register your models here.
@admin.register(User)
class UserAdmin(BaseAdmin):
    form = ChangeForm
    add_form = CreationForm

    list_display = ("phone_number", "fcm_token")
    list_filter = (
        "is_admin",
        "is_active",
    )
    search_fields = ("phone_number",)
    readonly_fields = ("last_login",)
    ordering = ("phone_number",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (
            "Main",
            {"fields": ("phone_number", "fcm_token")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "last_login",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                    "password_confirm",
                )
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields["is_superuser"].disabled = True
        return form
