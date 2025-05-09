from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ProfileUpdateView, DashboardView, ChangePasswordView, ProfessionalListView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),  
    path('professionals/', ProfessionalListView.as_view(), name='professional-list'),

]
