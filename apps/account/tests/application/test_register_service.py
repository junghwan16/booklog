"""Unit tests for RegisterUserService (application layer)."""

import pytest

from apps.account.application.ports.inbound.register_user import RegisterUserCommand
from apps.account.application.services.register_user_service import (
    RegisterUserService,
)
from apps.account.domain.exceptions import DuplicateEmailError


def test_register_success(user_repo, email_sender, token_repo):
    # 서비스 인스턴스 생성
    service = RegisterUserService(
        user_repo=user_repo,
        email_sender=email_sender,
        token_repo=token_repo,
    )

    # 실행할 커맨드
    command = RegisterUserCommand(
        email="test@example.com",
        nickname="tester",
        password="a_raw_password",
    )

    # 서비스 실행
    user_id = service.execute(command)

    # 검증: ID가 반환되고, 사용자가 저장되었는지 확인
    assert user_id is not None
    saved_user = user_repo.find_by_id(user_id)
    assert saved_user is not None
    assert saved_user.email == "test@example.com"

    # 검증: 이메일 인증 토큰이 발급되고, 이메일이 발송되었는지 확인
    assert email_sender.sent
    sent_email, sent_token = email_sender.sent[0]
    assert sent_email == "test@example.com"
    assert sent_token == f"email_verify:{user_id}"


def test_register_duplicate_email_raises_error(user_repo, email_sender, token_repo):
    # 서비스 인스턴스 생성
    service = RegisterUserService(
        user_repo=user_repo,
        email_sender=email_sender,
        token_repo=token_repo,
    )

    # 실행할 커맨드
    command = RegisterUserCommand(
        email="duplicate@example.com",
        nickname="tester",
        password="a_raw_password",
    )

    # 첫 번째 실행은 성공해야 함
    service.execute(command)

    # 두 번째 실행은 DuplicateEmailError를 발생시켜야 함
    with pytest.raises(DuplicateEmailError):
        service.execute(command)
