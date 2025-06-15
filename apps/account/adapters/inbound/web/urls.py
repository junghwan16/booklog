from django.urls import path
from .views import (
    auth_views,
    register_views,
    profile_views,
    password_views,
    verify_views,
)

app_name = "account"

urlpatterns = [
    # AUTH
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path("signup/", register_views.register_view, name="register"),
    # EMAIL VERIFICATION
    path("email/verify/<str:token>/", verify_views.verify_view, name="verify"),
    path(
        "email/verification-needed/",
        verify_views.verification_required_view,
        name="verification_required",
    ),
    # USER PROFILE
    path("profile/", profile_views.profile_view, name="profile"),
    path("profile/delete/", profile_views.delete_account_view, name="delete_account"),
    # PASSWORD MANAGEMENT
    path("password/change/", password_views.change_view, name="change_password"),
    path("password/forgot/", password_views.request_reset_view, name="password_reset"),
    path(
        "password/reset/<uidb64>/<token>/",
        password_views.reset_view,
        name="password_reset_confirm",
    ),
]
