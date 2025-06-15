import abc
from typing import List, Optional

from apps.book.domain.entities import UserBook, UserBookStatus


class UserBookRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, user_book: UserBook) -> UserBook:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, user_book_id: str) -> Optional[UserBook]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_for_user(self, user_id: str) -> List[UserBook]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_user_id_and_status(
        self, user_id: str, status: UserBookStatus
    ) -> List[UserBook]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user_book_id: str) -> None:
        raise NotImplementedError
