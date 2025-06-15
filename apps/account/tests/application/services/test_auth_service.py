import pytest

from apps.account.application.ports.inbound.authenticate_user import (
    AuthenticateUserCommand,
)
from apps.account.application.services.auth_service import AuthenticateUserService
from apps.account.domain.models import Account
from apps.account.domain.exceptions import InvalidCredentials
from apps.account.tests.fakes.fake_authenticator import FakeAuthenticator
from apps.account.tests.fakes.fake_user_repo import FakeUserRepository


@pytest.fixture
def user_repo():
    repo = FakeUserRepository()
    account = Account(
        id=1,
        email="test@example.com",
        nickname="testuser",
        is_email_verified=True,
    )
    repo.save(account)
    return repo


def test_authenticate_user_successfully(user_repo):
    # Arrange
    authenticator = FakeAuthenticator(user_repo=user_repo)
    service = AuthenticateUserService(authenticator=authenticator)
    command = AuthenticateUserCommand(
        email="test@example.com",
        password="testuser-password",  # See FakeUserRepository.check_password
    )

    # Act
    account = service.execute(command)

    # Assert
    assert account is not None
    assert account.id == 1
    assert account.email == "test@example.com"


def test_authenticate_user_with_invalid_credentials(user_repo):
    # Arrange
    authenticator = FakeAuthenticator(user_repo=user_repo)
    service = AuthenticateUserService(authenticator=authenticator)
    command = AuthenticateUserCommand(
        email="test@example.com", password="wrong-password"
    )

    # Act & Assert
    with pytest.raises(InvalidCredentials):
        service.execute(command)
