from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    # API Endpoints
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("otp-login/", views.OTPLoginView.as_view(), name="otp-login"),
    path("otp-verify/", views.OTPVerifyView.as_view(), name="otp-verify"),
    path("email-verify/", views.EmailVerificationView.as_view(), name="email-verify"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile-update/", views.ProfileUpdateView.as_view(), name="profile-update"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("professionals/", views.ProfessionalListView.as_view(), name="professionals"),
    # Template Views
    path("signup/", views.Signup_view, name="signup"),
    path("custom-login/", views.custom_login_view, name="custom-login"),
    path("logout-template/", views.logout_view, name="logout-template"),
    path(
        "profile-update-template/",
        views.profile_update_view,
        name="profile-update-template",
    ),
    path(
        "professional-detail/<int:pk>/",
        views.professional_detail_view,
        name="professional-detail",
    ),
    path("newsfeed/", views.newsfeed_view, name="newsfeed"),
]
