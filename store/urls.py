from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from orders.views import stripe_webhook_view
from products.views import IndexView

schema_view = get_swagger_view(title='Pastebin API')
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("products/", include("products.urls", namespace="products")),
    path("users/", include("users.urls", namespace="users")),
    path('accounts/', include('allauth.urls')),
    path("orders/", include("orders.urls", namespace="orders")),
    path('webhooks/stripe', stripe_webhook_view, name='stripe_webhook'),
    path('api/', include("api.urls", namespace='api')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
