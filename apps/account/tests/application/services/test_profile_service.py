import pytest

from apps.account.application.ports.inbound.update_profile import UpdateProfileCommand
from apps.account.application.services.profile_service import (
    GetProfileService,
    UpdateProfileService,
)
from apps.account.domain.exceptions import NotFoundError
from apps.account.domain.models import Account
from apps.account.tests.fakes.fake_user_repo import FakeUserRepository


@pytest.fixture
def user_repo():
    repo = FakeUserRepository()
    account = Account(id=1, email="test@example.com", nickname="testuser")
    repo.save(account)
    return repo


def test_get_profile_successfully(user_repo):
    service = GetProfileService(user_repo=user_repo)

    profile = service.execute(user_id=1)

    assert profile.id == 1
    assert profile.email == "test@example.com"
    assert profile.nickname == "testuser"


def test_get_profile_for_nonexistent_user():
    user_repo = FakeUserRepository()
    service = GetProfileService(user_repo=user_repo)

    with pytest.raises(NotFoundError):
        service.execute(user_id=999)


def test_update_profile_successfully(user_repo):
    service = UpdateProfileService(user_repo=user_repo)
    command = UpdateProfileCommand(user_id=1, nickname="updated_nickname")

    service.execute(command)

    updated_user = user_repo.find_by_id(1)
    assert updated_user.nickname == "updated_nickname"


def test_update_profile_for_nonexistent_user():
    user_repo = FakeUserRepository()
    service = UpdateProfileService(user_repo=user_repo)
    command = UpdateProfileCommand(user_id=999, nickname="new_nickname")

    with pytest.raises(NotFoundError):
        service.execute(command)
