import pytest

from apps.account.application.ports.inbound.change_password import ChangePasswordCommand
from apps.account.application.ports.inbound.request_password_reset import (
    RequestPasswordResetCommand,
)
from apps.account.application.ports.inbound.reset_password import ResetPasswordCommand
from apps.account.application.services.password_service import (
    ChangePasswordService,
    RequestPasswordResetService,
    ResetPasswordService,
)
from apps.account.domain.exceptions import InvalidCredentials, InvalidTokenError
from apps.account.domain.models import Account
from apps.account.tests.fakes.fake_email_sender import FakeEmailSender
from apps.account.tests.fakes.fake_token_repo import FakeTokenRepository
from apps.account.tests.fakes.fake_user_repo import FakeUserRepository


@pytest.fixture
def user_repo():
    repo = FakeUserRepository()
    account = Account(id=1, email="test@example.com", nickname="testuser")
    repo.save(account)
    return repo


def test_change_password_successfully(user_repo):
    service = ChangePasswordService(user_repo=user_repo)
    command = ChangePasswordCommand(
        user_id=1, old_password="testuser-password", new_password="new-password"
    )
    service.execute(command)
    # No exception means success


def test_change_password_with_invalid_credentials(user_repo):
    service = ChangePasswordService(user_repo=user_repo)
    command = ChangePasswordCommand(
        user_id=1, old_password="wrong-password", new_password="new-password"
    )
    with pytest.raises(InvalidCredentials):
        service.execute(command)


def test_request_password_reset_successfully(user_repo):
    token_repo = FakeTokenRepository()
    email_sender = FakeEmailSender()
    service = RequestPasswordResetService(
        user_repo=user_repo, token_repo=token_repo, email_sender=email_sender
    )
    command = RequestPasswordResetCommand(email="test@example.com")
    service.execute(command)

    assert len(email_sender.sent_password_resets) == 1
    sent_email = email_sender.sent_password_resets[0]
    assert sent_email[0] == "test@example.com"
    assert sent_email[1] == "1"  # UID
    assert sent_email[2] is not None  # Token


def test_reset_password_successfully(user_repo):
    token_repo = FakeTokenRepository()
    service = ResetPasswordService(user_repo=user_repo, token_repo=token_repo)
    token = token_repo.issue(user_id=1, purpose="pwd_reset")
    command = ResetPasswordCommand(user_id=1, token=token, new_password="new-password")

    service.execute(command)


def test_reset_password_with_invalid_token(user_repo):
    token_repo = FakeTokenRepository()
    service = ResetPasswordService(user_repo=user_repo, token_repo=token_repo)
    command = ResetPasswordCommand(
        user_id=1, token="invalid-token", new_password="new-password"
    )
    with pytest.raises(InvalidTokenError):
        service.execute(command)
