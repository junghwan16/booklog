from __future__ import annotations
from typing import Optional

from django.contrib.auth import authenticate

from apps.account.application.ports.outbound.authenticator import AuthenticatorPort
from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.domain.models import Account


class DjangoAuthenticator(AuthenticatorPort):
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def authenticate(self, email: str, password: str) -> Optional[Account]:
        user = authenticate(username=email, password=password)
        if user is not None:
            # Django's authenticate returns a Django user model.
            # We need to fetch our domain model.
            return self._user_repo.find_by_email(email)
        return None
