from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from apps.account.domain.models import Account


class AuthenticatorPort(ABC):
    @abstractmethod
    def authenticate(self, email: str, password: str) -> Optional[Account]:
        raise NotImplementedError
