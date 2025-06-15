from django.urls import path
from .views import auth_views, register_views, profile_views, password_views

urlpatterns = [
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path("register/", register_views.register_view, name="register"),
    path("profile/", profile_views.profile_view, name="profile"),
    path("password/change/", password_views.change_view, name="change_password"),
    path("password/reset/", password_views.request_reset_view, name="password_reset"),
    path(
        "password/reset/<uidb64>/<token>/",
        password_views.reset_view,
        name="password_reset_confirm",
    ),
]
