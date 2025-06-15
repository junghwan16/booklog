from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from apps.account.adapters.inbound.web.forms.register_forms import RegisterForm
from apps.account.application.ports.inbound.register_user import RegisterUserCommand
from apps.account.domain.exceptions import DuplicateEmailError
from apps.account.application.services.register_user_service import RegisterUserService

from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)
from apps.account.adapters.outbound.email.django_email_sender import DjangoEmailSender
from apps.account.adapters.outbound.persistence.django_token_repo import (
    DjangoTokenRepository,
)

_register_user_service = RegisterUserService(
    user_repo=DjangoUserRepository(),
    email_sender=DjangoEmailSender(),
    token_repo=DjangoTokenRepository(),
)


def register_view(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cmd = RegisterUserCommand(
                email=form.cleaned_data["email"],
                nickname=form.cleaned_data["nickname"],
                password=form.cleaned_data["password"],
            )
            try:
                _register_user_service.execute(cmd)
                messages.success(
                    request,
                    "가입 완료! 인증 메일을 확인해 주세요.",
                )
                return redirect("account:login")
            except DuplicateEmailError:
                form.add_error("email", "이미 가입된 이메일입니다.")
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})
