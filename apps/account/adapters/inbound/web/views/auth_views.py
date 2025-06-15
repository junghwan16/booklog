from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest
from apps.account.adapters.inbound.web.forms.auth_forms import LoginForm
from apps.account.adapters.outbound.security.django_session_manager import (
    DjangoSessionManager,
)
from apps.account.adapters.outbound.security.django_authenticator import (
    DjangoAuthenticator,
)
from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)
from apps.account.application.ports.inbound.authenticate_user import (
    AuthenticateUserCommand,
)
from apps.account.application.services.auth_service import (
    AuthenticateUserService,
    LogoutUserService,
)
from apps.account.domain.exceptions import InvalidCredentials


_session_manager = DjangoSessionManager()
_user_repo = DjangoUserRepository()
_authenticator = DjangoAuthenticator(user_repo=_user_repo)
_auth_service = AuthenticateUserService(authenticator=_authenticator)
_logout_service = LogoutUserService(session_manager=_session_manager)


def login_view(request: HttpRequest):
    next_url = request.GET.get("next") or reverse("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cmd = AuthenticateUserCommand(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            try:
                account = _auth_service.execute(cmd)
                # Login must happen before we can access request.user
                _session_manager.login(request, account.id)

                if not account.is_email_verified:
                    return redirect("verification_required")

                return redirect(next_url)
            except InvalidCredentials:
                messages.error(request, "이메일 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def logout_view(request: HttpRequest):
    _logout_service.execute(request)
    messages.info(request, "로그아웃되었습니다.")
    return redirect("home")
