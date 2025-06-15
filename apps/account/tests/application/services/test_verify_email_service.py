import pytest

from apps.account.application.services.verify_email_service import VerifyEmailService
from apps.account.application.services.resend_verification_email_service import (
    ResendVerificationEmailService,
)
from apps.account.domain.exceptions import InvalidTokenError, UserNotFoundError
from apps.account.domain.models import Account
from apps.account.tests.fakes.fake_email_sender import FakeEmailSender
from apps.account.tests.fakes.fake_token_repo import FakeTokenRepository
from apps.account.tests.fakes.fake_user_repo import FakeUserRepository


@pytest.fixture
def user_repo():
    repo = FakeUserRepository()
    account = Account(
        id=1, email="test@example.com", nickname="testuser", is_email_verified=False
    )
    repo.save(account)
    return repo


def test_verify_email_successfully(user_repo):
    token_repo = FakeTokenRepository()
    service = VerifyEmailService(user_repo=user_repo, token_repo=token_repo)

    # Issue a token for the user
    token = token_repo.issue(user_id=1, purpose="email_verify")

    # Verify email
    service.execute(token)

    # Check that user is now verified
    user = user_repo.find_by_id(1)
    assert user.is_email_verified is True


def test_verify_email_with_invalid_token(user_repo):
    token_repo = FakeTokenRepository()
    service = VerifyEmailService(user_repo=user_repo, token_repo=token_repo)

    with pytest.raises(InvalidTokenError):
        service.execute("invalid-token")


def test_resend_verification_email_successfully(user_repo):
    token_repo = FakeTokenRepository()
    email_sender = FakeEmailSender()
    service = ResendVerificationEmailService(
        user_repo=user_repo, email_sender=email_sender, token_repo=token_repo
    )

    service.execute("test@example.com")

    assert len(email_sender.sent_emails) == 1
    sent_email = email_sender.sent_emails[0]
    assert sent_email[0] == "test@example.com"


def test_resend_verification_email_for_nonexistent_user():
    user_repo = FakeUserRepository()
    token_repo = FakeTokenRepository()
    email_sender = FakeEmailSender()
    service = ResendVerificationEmailService(
        user_repo=user_repo, email_sender=email_sender, token_repo=token_repo
    )

    with pytest.raises(UserNotFoundError):
        service.execute("nonexistent@example.com")


def test_resend_verification_email_for_already_verified_user():
    user_repo = FakeUserRepository()
    verified_account = Account(
        id=1, email="test@example.com", nickname="testuser", is_email_verified=True
    )
    user_repo.save(verified_account)

    token_repo = FakeTokenRepository()
    email_sender = FakeEmailSender()
    service = ResendVerificationEmailService(
        user_repo=user_repo, email_sender=email_sender, token_repo=token_repo
    )

    # Should not send email for already verified user
    service.execute("test@example.com")

    assert len(email_sender.sent_emails) == 0
