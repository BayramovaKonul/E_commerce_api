from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = i18n_patterns (
    path(_("admin/"), admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)