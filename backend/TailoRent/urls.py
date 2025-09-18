from django.contrib import admin
from django.urls import path, include
from profiles.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='home'),  # Homepage
    path('admin/', admin.site.urls),
    path('api/profiles/', include('profiles.urls')), 
    path('api/bookings/', include('bookings.urls')),
    path('api/marketplace/', include('marketplace.urls', namespace='marketplace')),  # ✅ Fix
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 