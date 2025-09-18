from django.urls import path
from .views import (
    # API Views
    RegistrationView, LoginView, LogoutView, ProfileUpdateView,
    DashboardView, ChangePasswordView, ProfessionalListView,

    # Template Views
    Signup_view, CustomLoginView, dashboard_view, profile_update_view,
    professional_list_view, about_view, logout_view, professional_detail_view
)

urlpatterns = [
    # API Views
    path('api/signup/', RegistrationView.as_view(), name='api_signup'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/update-profile/', ProfileUpdateView.as_view(), name='api_update_profile'),
    path('api/dashboard/', DashboardView.as_view(), name='api_dashboard'),
    path('api/change-password/', ChangePasswordView.as_view(), name='api_change_password'),
    path('api/professionals/', ProfessionalListView.as_view(), name='api_professionals'),

    # HTML Template Views
    path('signup/', Signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile_update/', profile_update_view, name='profile_update'),
    path('professionals/', professional_list_view, name='professional_list'),
     path('professionals/<int:pk>/', professional_detail_view, name='professional_detail'),
    path('about/', about_view, name='about'),
]
