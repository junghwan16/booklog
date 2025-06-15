import pytest

from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)
from apps.account.domain.models import Account, AccountStatus


@pytest.fixture
def user_repo():
    return DjangoUserRepository()


@pytest.fixture
def new_account():
    return Account(
        id=None,
        email="test@example.com",
        nickname="testuser",
        password="a_raw_password",
    )


@pytest.mark.django_db
class TestDjangoUserRepository:
    def test_save_new_account_and_find(self, user_repo, new_account):
        # 새로운 계정 저장
        user_id = user_repo.save(new_account)
        assert isinstance(user_id, int)

        # ID로 계정 조회
        found_by_id = user_repo.find_by_id(user_id)
        assert found_by_id is not None
        assert found_by_id.id == user_id
        assert found_by_id.email == new_account.email
        assert found_by_id.nickname == new_account.nickname
        assert found_by_id.is_email_verified is False
        assert found_by_id.status == AccountStatus.ACTIVE

        # 이메일로 계정 조회
        found_by_email = user_repo.find_by_email(new_account.email)
        assert found_by_email is not None
        assert found_by_email.id == user_id

    def test_exists_by_email(self, user_repo, new_account):
        assert user_repo.exists_by_email(new_account.email) is False
        user_repo.save(new_account)
        assert user_repo.exists_by_email(new_account.email) is True

    def test_update_existing_account(self, user_repo, new_account):
        user_id = user_repo.save(new_account)

        # 계정 정보 수정
        account_to_update = Account(
            id=user_id,
            email="test@example.com",
            nickname="new_nickname",
            is_email_verified=True,
            status=AccountStatus.DELETED,
        )
        user_repo.save(account_to_update)

        # 수정된 정보 확인
        updated_account = user_repo.find_by_id(user_id)
        assert updated_account is not None
        assert updated_account.nickname == "new_nickname"
        assert updated_account.is_email_verified is True
        assert updated_account.is_active is False

    def test_password_handling(self, user_repo, new_account):
        user_id = user_repo.save(new_account)

        # 비밀번호 확인
        assert user_repo.check_password(user_id, "a_raw_password") is True
        assert user_repo.check_password(user_id, "wrong_password") is False

        # 비밀번호 변경
        user_repo.change_password(user_id, "a_new_password")

        # 새 비밀번호로 확인
        assert user_repo.check_password(user_id, "a_raw_password") is False
        assert user_repo.check_password(user_id, "a_new_password") is True
