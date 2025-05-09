# bookings/urls.py (updated)
from django.urls import path
from .views import (
    BookingListCreateView,
    ProfessionalBookingsView,
    BookingDetailView,
    UpdateBookingStatusView,
    ProfessionalDashboardView, CustomerDashboardView
)

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='customer-bookings'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('professional/', ProfessionalBookingsView.as_view(), name='professional-bookings'),
    path('<int:pk>/update-status/', UpdateBookingStatusView.as_view(), name='update-booking-status'), 
    path('dashboard/', ProfessionalDashboardView.as_view(), name='professional-dashboard'),
    path('customer/dashboard/', CustomerDashboardView.as_view(), name='customer-dashboard'),

]
