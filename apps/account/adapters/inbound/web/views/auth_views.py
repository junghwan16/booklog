from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest
from apps.account.adapters.inbound.web.forms.auth_forms import LoginForm
from apps.account.application.ports.inbound.authenticate_user import (
    AuthenticateUserCommand,
)
from apps.account.application import containers as containers
from apps.account.domain.exceptions import InvalidCredentials


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
                containers.auth_service.execute(cmd, request)
                return redirect(next_url)
            except InvalidCredentials:
                messages.error(request, "이메일 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def logout_view(request: HttpRequest):
    containers.logout_service.execute(request)
    messages.info(request, "로그아웃되었습니다.")
    return redirect("home")
