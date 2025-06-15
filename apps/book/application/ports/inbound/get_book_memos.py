from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from apps.book.domain.entities import Memo


@dataclass(frozen=True, slots=True)
class GetBookMemosQuery:
    """Query to get memos for a specific book."""

    user_id: str
    user_book_id: str


class GetBookMemosUseCase(ABC):
    """Interface for getting memos for a book."""

    @abstractmethod
    def execute(self, query: GetBookMemosQuery) -> List[Memo]:
        """Execute get book memos use case."""
        ...
