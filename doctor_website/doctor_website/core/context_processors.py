from .models import SiteSettings


def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings()
    except Exception:
        settings = SiteSettings()
    return {'site': settings}
