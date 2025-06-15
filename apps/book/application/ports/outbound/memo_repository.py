import abc
from typing import List, Optional
from apps.book.domain.entities import Memo


class MemoRepository(abc.ABC):

    @abc.abstractmethod
    def save(self, memo: Memo) -> Memo:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, memo_id: str) -> Optional[Memo]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_user_book_id(self, user_book_id: str) -> List[Memo]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, memo_id: str) -> None:
        raise NotImplementedError
