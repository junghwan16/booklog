from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest

from apps.account.adapters.inbound.web.forms.profile_forms import ProfileForm
from apps.account.application.ports.inbound.update_profile import UpdateProfileCommand
from apps.account.application.services.profile_service import (
    GetProfileService,
    UpdateProfileService,
)
from apps.account.domain.exceptions import NotFoundError

from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)

_repo = DjangoUserRepository()

_get_service = GetProfileService(_repo)
_update_service = UpdateProfileService(_repo)


@login_required
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
        form = ProfileForm(initial={"nickname": acc.nickname.value})

    context = {
        "form": form,
        "account": acc,
    }
    return render(request, "account/profile.html", context)
