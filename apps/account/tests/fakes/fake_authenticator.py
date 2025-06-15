from __future__ import annotations
from typing import Optional

from apps.account.application.ports.outbound.authenticator import AuthenticatorPort
from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.domain.models import Account


class FakeAuthenticator(AuthenticatorPort):
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def authenticate(self, email: str, password: str) -> Optional[Account]:
        user = self._user_repo.find_by_email(email)
        if user and self._user_repo.check_password(user.id, password):
            return user
        return None
