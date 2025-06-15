from __future__ import annotations
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from apps.account.application.services.verify_email_service import VerifyEmailService
from apps.account.domain.exceptions import InvalidTokenError, UserNotFoundError
from apps.account.adapters.inbound.web.forms.verify_forms import (
    ResendVerificationEmailForm,
)
from apps.account.application.services.resend_verification_email_service import (
    ResendVerificationEmailService,
)

from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)
from apps.account.adapters.outbound.persistence.django_token_repo import (
    DjangoTokenRepository,
)
from apps.account.adapters.outbound.email.django_email_sender import DjangoEmailSender


_verify_email_service = VerifyEmailService(
    DjangoUserRepository(),
    DjangoTokenRepository(),
)

_resend_verification_email_service = ResendVerificationEmailService(
    DjangoUserRepository(),
    DjangoEmailSender(),
    DjangoTokenRepository(),
)


def verify_view(request: HttpRequest, token: str):
    try:
        _verify_email_service.execute(token)
        return render(request, "account/email_verified.html")
    except InvalidTokenError:
        messages.error(request, "유효하지 않거나 만료된 토큰입니다.")
        return redirect("account:login")


@login_required
def verification_required_view(request: HttpRequest):
    if request.user.is_email_verified:
        return redirect("home")

    if request.method == "POST":
        try:
            _resend_verification_email_service.execute(request.user.email)
            messages.success(
                request, "인증 이메일을 다시 보냈습니다. 받은 편지함을 확인해 주세요."
            )
        except UserNotFoundError:
            # Should not happen for a logged-in user
            messages.error(request, "사용자를 찾을 수 없습니다.")
        return redirect("account:verification_required")

    return render(request, "account/verification_required.html")


def resend_verification_email_view(request: HttpRequest):
    if request.method == "POST":
        form = ResendVerificationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                _resend_verification_email_service.execute(email)
                messages.success(
                    request,
                    "인증 이메일을 다시 보냈습니다. 받은 편지함을 확인해 주세요.",
                )
            except UserNotFoundError:
                messages.error(request, "해당 이메일로 가입된 계정을 찾을 수 없습니다.")
            return redirect("account:login")
    else:
        form = ResendVerificationEmailForm()
    return render(request, "account/resend_verification_email.html", {"form": form})
