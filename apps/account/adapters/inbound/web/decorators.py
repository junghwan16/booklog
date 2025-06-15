from functools import wraps
from django.shortcuts import redirect
from django.http import HttpRequest


def email_verified_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account:login")
        if not request.user.is_email_verified:
            return redirect("account:verification_required")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
