from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="E-commerce",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   url="https://epicbazaar.store/",
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = i18n_patterns (
    path(_("admin/"), admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('user/', include('account.urls')),
    path('store/', include('store.urls')),
    path('products/', include('products.urls')),
    path('shopping/', include('e_commerce.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)