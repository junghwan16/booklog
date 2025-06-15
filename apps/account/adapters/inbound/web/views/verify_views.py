from __future__ import annotations
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpRequest
from apps.account.application.services.verify_email_service import VerifyEmailService
from apps.account.domain.exceptions import InvalidTokenError

from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)
from apps.account.adapters.outbound.persistence.django_token_repo import (
    DjangoTokenRepository,
)

_verify_service = VerifyEmailService(
    DjangoUserRepository(),
    DjangoTokenRepository(),
)


def verify_view(request: HttpRequest, token: str):
    try:
        _verify_service.execute(token)
        messages.success(request, "이메일 인증이 완료되었습니다. 로그인해 주세요.")
    except InvalidTokenError:
        messages.error(request, "유효하지 않거나 만료된 토큰입니다.")
    return redirect("login")
