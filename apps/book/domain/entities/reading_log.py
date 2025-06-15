from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
import uuid
from typing import Optional


@dataclass
class ReadingLog:
    """일일 독서 기록 (독서 잔디의 데이터 소스)"""

    user_book_id: str
    user_id: str
    date: date
    start_page: int
    end_page: int
    note: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)

    def __post_init__(self):
        if self.start_page > self.end_page:
            raise ValueError("Start page cannot be greater than end page.")

    @property
    def pages_read(self) -> int:
        return self.end_page - self.start_page
