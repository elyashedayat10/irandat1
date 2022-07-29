from .models import Setting


def setting(request):
    return {
        "setting": Setting.load(),
    }
