from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class UserBookStatus(Enum):
    TO_READ = "읽을 책"
    READING = "읽는 중"
    FINISHED = "다 읽음"


@dataclass
class UserBook:
    """사용자가 직접 입력한 책"""
    
    # 책 정보 (사용자가 직접 입력)
    title: str
    author: str
    total_pages: int
    
    # 사용자 관련 정보
    user_id: str
    status: UserBookStatus = UserBookStatus.TO_READ
    current_page: int = 0
    
    # 메타데이터
    id: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    created_at: Optional[datetime] = field(default=None, kw_only=True)
    updated_at: Optional[datetime] = field(default=None, kw_only=True)
    
    # 선택적 정보
    publisher: Optional[str] = field(default=None, kw_only=True)
    isbn: Optional[str] = field(default=None, kw_only=True)
    cover_image_url: Optional[str] = field(default=None, kw_only=True)

    def __post_init__(self):
        if not self.title or not self.author:
            raise ValueError("Title and author are required.")
        if self.total_pages <= 0:
            raise ValueError("Total pages must be positive.")
        if self.current_page < 0:
            raise ValueError("Current page cannot be negative.")
        if self.current_page > self.total_pages:
            raise ValueError("Current page cannot exceed total pages.")

    @property
    def progress_percentage(self) -> float:
        """읽기 진행률 (0-100%)"""
        if self.total_pages == 0:
            return 0.0
        return (self.current_page / self.total_pages) * 100

    @property
    def is_finished(self) -> bool:
        """완독 여부"""
        return self.current_page >= self.total_pages

    def update_progress(self, current_page: int) -> None:
        """읽기 진행도 업데이트"""
        if current_page < 0:
            raise ValueError("Current page cannot be negative.")
        if current_page > self.total_pages:
            raise ValueError("Current page cannot exceed total pages.")
        
        self.current_page = current_page
        
        # 자동으로 상태 업데이트
        if current_page >= self.total_pages:
            self.status = UserBookStatus.FINISHED
        elif current_page > 0 and self.status == UserBookStatus.TO_READ:
            self.status = UserBookStatus.READING

    def start_reading(self) -> None:
        """읽기 시작"""
        if self.status == UserBookStatus.TO_READ:
            self.status = UserBookStatus.READING

    def mark_as_finished(self) -> None:
        """완독 처리"""
        self.current_page = self.total_pages
        self.status = UserBookStatus.FINISHED

    def touch(self):
        self.updated_at = datetime.now()
