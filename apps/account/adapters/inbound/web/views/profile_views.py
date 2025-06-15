from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from apps.account.adapters.inbound.web.decorators import email_verified_required

from apps.account.adapters.inbound.web.forms.profile_forms import (
    ProfileForm,
    DeleteAccountForm,
)
from apps.account.application.ports.inbound.update_profile import UpdateProfileCommand
from apps.account.application.services.profile_service import (
    GetProfileService,
    UpdateProfileService,
)
from apps.account.application.services.delete_account_service import (
    DeleteAccountService,
)
from apps.account.domain.exceptions import NotFoundError, InvalidCredentials

from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)
from apps.account.adapters.outbound.security.django_session_manager import (
    DjangoSessionManager,
)

_repo = DjangoUserRepository()
_session_manager = DjangoSessionManager()

_get_service = GetProfileService(_repo)
_update_service = UpdateProfileService(_repo)
_delete_service = DeleteAccountService(_repo)


@email_verified_required
def profile_view(request: HttpRequest):
    acc = _get_service.execute(request.user.id)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cmd = UpdateProfileCommand(
                user_id=request.user.id,
                nickname=form.cleaned_data["nickname"] or None,
            )
            try:
                _update_service.execute(cmd)
                messages.success(request, "프로필이 업데이트되었습니다.")
                return redirect("profile")
            except NotFoundError:
                messages.error(request, "계정을 찾을 수 없습니다.")
    else:
        form = ProfileForm(initial={"nickname": acc.nickname})

    context = {
        "form": form,
        "account": acc,
    }
    return render(request, "account/profile.html", context)


@email_verified_required
def delete_account_view(request: HttpRequest):
    if request.method == "POST":
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]

            # 비밀번호 확인
            if not _repo.check_password(request.user.id, password):
                form.add_error("password", "비밀번호가 올바르지 않습니다.")
            else:
                try:
                    # 계정 삭제
                    _delete_service.execute(request.user.id)
                    # 세션에서 로그아웃
                    _session_manager.logout(request)
                    messages.success(request, "계정이 성공적으로 삭제되었습니다.")
                    return redirect("home")
                except Exception as e:
                    messages.error(request, "계정 삭제 중 오류가 발생했습니다.")
    else:
        form = DeleteAccountForm()

    return render(request, "account/delete_account.html", {"form": form})
