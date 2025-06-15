from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Optional


@dataclass
class Memo:
    """책에 대한 사용자 메모"""

    user_book_id: str
    user_id: str
    content: str
    page: Optional[int] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default_factory=datetime.now, kw_only=True)

    def __post_init__(self):
        if not self.content:
            raise ValueError("Memo content cannot be empty.")

    def update(self, new_content: str, new_page: Optional[int]):
        self.content = new_content
        self.page = new_page
        self.updated_at = datetime.now()
