from abc import ABC, abstractmethod

from apps.account.domain.models import Account


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Account | None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Account | None: ...

    @abstractmethod
    def exists_by_email(self, email: str) -> bool: ...

    @abstractmethod
    def save(self, user: Account) -> int: ...

    @abstractmethod
    def check_password(self, user_id: int, raw_password: str) -> bool: ...

    @abstractmethod
    def change_password(self, user_id: int, new_raw_password: str) -> None: ...

    @abstractmethod
    def delete(self, user_id: int) -> None: ...
