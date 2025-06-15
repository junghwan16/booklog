from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from apps.account.adapters.inbound.web.forms.password_forms import (
    ChangePasswordForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from apps.account.application.ports.inbound.change_password import ChangePasswordCommand
from apps.account.application.ports.inbound.request_password_reset import (
    RequestPasswordResetCommand,
)
from apps.account.application.ports.inbound.reset_password import ResetPasswordCommand
from apps.account.application import containers
from apps.account.domain.exceptions import InvalidCredentials, InvalidTokenError


@login_required
def change_view(request: HttpRequest):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cmd = ChangePasswordCommand(
                user_id=request.user.id,
                old_password=form.cleaned_data["old_password"],
                new_password=form.cleaned_data["new_password"],
            )
            try:
                containers.change_password_service.execute(cmd)
                messages.success(request, "비밀번호가 변경되었습니다.")
                return redirect("profile")
            except InvalidCredentials:
                form.add_error("old_password", "현재 비밀번호가 올바르지 않습니다.")
    else:
        form = ChangePasswordForm()
    return render(request, "account/change_password.html", {"form": form})


def request_reset_view(request: HttpRequest):
    if request.method == "POST":
        form = ResetPasswordRequestForm(request.POST)
        if form.is_valid():
            cmd = RequestPasswordResetCommand(email=form.cleaned_data["email"])
            containers.request_password_reset_service.execute(cmd)
            messages.info(request, "재설정 메일을 확인해 주세요.")
            return redirect("login")
    else:
        form = ResetPasswordRequestForm()
    return render(request, "account/password_reset_request.html", {"form": form})


def reset_view(request: HttpRequest, token: str):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            cmd = ResetPasswordCommand(
                token=token,
                new_password=form.cleaned_data["new_password"],
            )
            try:
                containers.reset_password_service.execute(cmd)
                messages.success(
                    request, "새 비밀번호가 설정되었습니다. 로그인해 주세요."
                )
                return redirect("login")
            except InvalidTokenError:
                messages.error(request, "토큰이 유효하지 않거나 만료되었습니다.")
                return redirect("password_reset")
    else:
        form = ResetPasswordForm()
    return render(request, "account/password_reset_form.html", {"form": form})
