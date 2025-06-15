from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(slots=True)
class DomainEvent:
    occurred_at: datetime = datetime.now(tz=timezone.utc)


@dataclass(slots=True)
class AccountRegistered(DomainEvent):
    account_id: int
    email: str


@dataclass(slots=True)
class EmailVerified(DomainEvent):
    account_id: int


@dataclass(slots=True)
class PasswordChanged(DomainEvent):
    account_id: int
