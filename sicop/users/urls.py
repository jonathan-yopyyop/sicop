from django.contrib.auth import views as auth_views
from django.urls import path

from sicop.users.views import (
    LoginView,
    ResetPasswordMessageView,
    ResetPasswordView,
    SignupView,
    UserPasswordChangeView,
    UserProfileView,
    logout_view,
)

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="user_login",
    ),
    path(
        "logout/",
        logout_view,
        name="user_logout",
    ),
    path(
        "signup/",
        SignupView.as_view(),
        name="user_signup",
    ),
    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="user_reset_password",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="sicop/users/reset/password_reset_confirm.html",
        ),
        name="user_password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="sicop/users/reset/password_reset_complete.html",
        ),
        name="user_password_reset_complete",
    ),
    path(
        "password-reset-done/",
        ResetPasswordMessageView.as_view(),
        name="user_password_reset_done",
    ),
    path(
        "profile/info/",
        UserProfileView.as_view(),
        name="user_profile",
    ),
    path(
        "profile/password/",
        UserPasswordChangeView.as_view(),
        name="user_password_change",
    ),
]
