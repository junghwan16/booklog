import pytest
from dataclasses import replace
from werkzeug.security import generate_password_hash, check_password_hash

from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.application.ports.outbound.email_sender import EmailSenderPort
from apps.account.application.ports.outbound.token_repo import TokenRepository


class InMemoryUserRepo(UserRepository):
    """Simple in-memory implementation of UserRepository for unit tests."""

    def __init__(self):
        self._data: dict[int, object] = {}
        self._next_id: int = 1

    # UserRepository interface
    def find_by_id(self, user_id: int):
        return self._data.get(user_id)

    def find_by_email(self, email: str):
        for acc in self._data.values():
            if str(acc.email) == email:
                return acc
        return None

    def exists_by_email(self, email: str) -> bool:
        return any(str(acc.email) == email for acc in self._data.values())

    def save(self, user):
        if user.id is None:
            user_id = self._next_id
            self._next_id += 1
            # In a real scenario, password would be hashed here.
            # For this fake repo, we'll store the hash of the raw password.
            hashed_password = generate_password_hash(user.password)
            user = replace(user, id=user_id, password=hashed_password)
        self._data[user.id] = user
        return user.id

    def check_password(self, user_id: int, raw_password: str) -> bool:
        user = self.find_by_id(user_id)
        if not user or not user.password:
            return False
        return check_password_hash(user.password, raw_password)

    def change_password(self, user_id: int, new_raw_password: str) -> None:
        user = self.find_by_id(user_id)
        if user:
            self._data[user_id] = replace(
                user, password=generate_password_hash(new_raw_password)
            )


class DummyEmailSender(EmailSenderPort):
    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send_email_verify(self, to_email: str, token: str) -> None:
        self.sent.append((to_email, token))

    def send_password_reset(self, to_email: str, token: str) -> None:
        self.sent.append((to_email, token))


class InMemoryTokenRepo(TokenRepository):
    def __init__(self):
        self._issued: dict[str, int] = {}

    def issue(self, user_id: int, *, purpose: str, ttl_sec: int | None = None) -> str:
        token = f"{purpose}:{user_id}"
        self._issued[token] = user_id
        return token

    def consume(self, token: str, *, purpose: str) -> int | None:
        return self._issued.pop(token, None)


@pytest.fixture()
def user_repo() -> InMemoryUserRepo:
    return InMemoryUserRepo()


@pytest.fixture()
def email_sender() -> DummyEmailSender:
    return DummyEmailSender()


@pytest.fixture()
def token_repo() -> InMemoryTokenRepo:
    return InMemoryTokenRepo()


@pytest.fixture()
def deps(user_repo, email_sender, token_repo):
    """Aggregated dependency bundle for convenience."""
    return {
        "user_repo": user_repo,
        "email_sender": email_sender,
        "token_repo": token_repo,
    }
