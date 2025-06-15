from __future__ import annotations
from typing import Dict, Optional
from dataclasses import replace

from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.domain.models import Account


class FakeUserRepository(UserRepository):
    def __init__(self, users: Dict[int, Account] | None = None):
        self._users = users or {}
        self._next_id = (max(self._users.keys()) + 1) if self._users else 1

    def find_by_id(self, user_id: int) -> Optional[Account]:
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[Account]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def exists_by_email(self, email: str) -> bool:
        return any(user.email == email for user in self._users.values())

    def save(self, account: Account) -> int:
        if account.id is None:
            new_id = self._next_id
            new_account = replace(account, id=new_id)
            self._users[new_id] = new_account
            self._next_id += 1
            return new_id
        else:
            self._users[account.id] = account
            return account.id

    def check_password(self, user_id: int, raw_password: str) -> bool:
        user = self.find_by_id(user_id)
        # For fake repo, we assume password matches if it's the same as nickname + "-password"
        return user is not None and raw_password == f"{user.nickname}-password"

    def change_password(self, user_id: int, new_raw_password: str) -> None:
        user = self.find_by_id(user_id)
        if user:
            # We don't actually store password in the fake domain model,
            # so this is a no-op for the fake.
            pass

    def delete(self, user_id: int) -> None:
        if user_id in self._users:
            del self._users[user_id]
