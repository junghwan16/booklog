import pytest

from apps.account.application.ports.inbound.register_user import RegisterUserCommand
from apps.account.application.services.register_user_service import RegisterUserService
from apps.account.domain.exceptions import DuplicateEmailError
from apps.account.tests.fakes.fake_email_sender import FakeEmailSender
from apps.account.tests.fakes.fake_token_repo import FakeTokenRepository
from apps.account.tests.fakes.fake_user_repo import FakeUserRepository


def test_register_user_successfully():
    # Arrange
    user_repo = FakeUserRepository()
    email_sender = FakeEmailSender()
    token_repo = FakeTokenRepository()
    service = RegisterUserService(user_repo, email_sender, token_repo)
    command = RegisterUserCommand(
        email="test@example.com",
        nickname="testuser",
        password="password123",
    )

    # Act
    user_id = service.execute(command)

    # Assert
    assert user_id == 1
    saved_user = user_repo.find_by_id(user_id)
    assert saved_user is not None
    assert saved_user.email == "test@example.com"
    assert not saved_user.is_email_verified

    # Assert email was sent
    assert len(email_sender.sent_emails) == 1
    sent_email = email_sender.sent_emails[0]
    assert sent_email[0] == "test@example.com"
    assert "token-for-1-with-purpose-email_verify" in sent_email[1]

    # Assert token was issued
    assert token_repo.consume(sent_email[1], "email_verify") == user_id


def test_register_user_with_duplicate_email_should_fail():
    # Arrange
    user_repo = FakeUserRepository()
    email_sender = FakeEmailSender()
    token_repo = FakeTokenRepository()
    service = RegisterUserService(user_repo, email_sender, token_repo)

    # Pre-populate user
    existing_command = RegisterUserCommand(
        email="test@example.com", nickname="existinguser", password="password123"
    )
    service.execute(existing_command)

    # New command with same email
    command = RegisterUserCommand(
        email="test@example.com", nickname="newuser", password="password456"
    )

    # Act & Assert
    with pytest.raises(DuplicateEmailError):
        service.execute(command)

    # Assert that no new user was created or email sent
    assert len(user_repo._users) == 1
    assert len(email_sender.sent_emails) == 1
