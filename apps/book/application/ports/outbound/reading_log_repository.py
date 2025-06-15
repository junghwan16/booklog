from abc import ABC, abstractmethod
from typing import List
from datetime import date

from apps.book.domain.entities import ReadingLog


class ReadingLogRepository(ABC):
    @abstractmethod
    def save(self, reading_log: ReadingLog) -> ReadingLog: ...

    @abstractmethod
    def get_by_user_book_id(self, user_book_id: str) -> List[ReadingLog]: ...

    @abstractmethod
    def get_by_user_id_and_date_range(
        self, user_id: str, start_date: date, end_date: date
    ) -> List[ReadingLog]: ...
