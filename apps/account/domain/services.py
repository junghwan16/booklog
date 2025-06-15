from typing import Tuple, List, Callable

from .models import Account
from .value_objects import Email, Nickname
from .events import AccountRegistered
from .exceptions import DuplicateEmailError


def register_account(
    email: Email,
    nickname: Nickname,
    password_hash: str,
    email_exists: Callable[[str], bool],
) -> Tuple[Account, List[AccountRegistered]]:
    """
    도메인 규칙: 이메일 중복 불가 → 이미 존재 시 예외
    `exists_email` 은 인프라 독립적인 콜백(Repository에서 주입)
    """
    if email_exists(str(email)):
        raise DuplicateEmailError(str(email))

    acc = Account(
        id=None,
        email=email,
        nickname=nickname,
        password_hash=password_hash,
    )
    event = AccountRegistered(account_id=-1, email=str(email))  # id는 저장단에서 교체
    return acc, [event]
