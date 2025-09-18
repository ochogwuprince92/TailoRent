"""
URL configuration for TailoRent project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import TemplateView


def api_root(request):
    """API root endpoint with available endpoints."""
    return JsonResponse(
        {
            "message": "Welcome to TailoRent API",
            "version": "1.0.0",
            "endpoints": {
                "profiles": "/api/profiles/",
                "bookings": "/api/bookings/",
                "marketplace": "/api/marketplace/",
                "admin": "/admin/",
                "docs": "/api/docs/",
            },
        }
    )


urlpatterns = [
    # API Root
    path("api/", api_root, name="api_root"),
    # Admin
    path("admin/", admin.site.urls),
    # API Endpoints
    path("api/profiles/", include("apps.profiles.urls")),
    path("api/bookings/", include("apps.bookings.urls")),
    path("api/marketplace/", include("apps.marketplace.urls")),
    # Documentation
    path(
        "api/docs/",
        TemplateView.as_view(
            template_name="api_docs.html",
            extra_context={"title": "TailoRent API Documentation"},
        ),
        name="api_docs",
    ),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
