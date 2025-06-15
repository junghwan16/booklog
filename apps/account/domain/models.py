from dataclasses import dataclass
from enum import Enum


class AccountStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"


@dataclass(frozen=True, slots=True)
class Account:
    """Pure domain entity - Django-agnostic"""

    id: int | None
    email: str
    nickname: str
    password: str | None = None
    is_email_verified: bool = False
    status: AccountStatus = AccountStatus.ACTIVE

    @property
    def is_active(self) -> bool:
        """Check if account is active"""
        return self.status == AccountStatus.ACTIVE
