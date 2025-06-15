import pytest

from apps.account.application.services.delete_account_service import (
    DeleteAccountService,
)
from apps.account.domain.models import Account
from apps.account.tests.fakes.fake_user_repo import FakeUserRepository


@pytest.fixture
def user_repo():
    repo = FakeUserRepository()
    account = Account(id=1, email="test@example.com", nickname="testuser")
    repo.save(account)
    return repo


def test_delete_account_successfully(user_repo):
    service = DeleteAccountService(user_repo=user_repo)

    # Verify user exists before deletion
    assert user_repo.find_by_id(1) is not None

    service.execute(user_id=1)

    # Verify user is deleted
    assert user_repo.find_by_id(1) is None


def test_delete_nonexistent_account():
    user_repo = FakeUserRepository()
    service = DeleteAccountService(user_repo=user_repo)

    # Should not raise an exception
    service.execute(user_id=999)


def test_delete_account_removes_user_completely(user_repo):
    service = DeleteAccountService(user_repo=user_repo)

    # Add another user to ensure only the target user is deleted
    another_account = Account(id=2, email="another@example.com", nickname="another")
    user_repo.save(another_account)

    # Verify both users exist
    assert user_repo.find_by_id(1) is not None
    assert user_repo.find_by_id(2) is not None

    # Delete first user
    service.execute(user_id=1)

    # Verify only first user is deleted
    assert user_repo.find_by_id(1) is None
    assert user_repo.find_by_id(2) is not None


def test_delete_account_by_email_lookup():
    user_repo = FakeUserRepository()
    service = DeleteAccountService(user_repo=user_repo)

    account = Account(id=1, email="test@example.com", nickname="testuser")
    user_repo.save(account)

    # Verify user can be found by email before deletion
    assert user_repo.find_by_email("test@example.com") is not None

    service.execute(user_id=1)

    # Verify user cannot be found by email after deletion
    assert user_repo.find_by_email("test@example.com") is None
