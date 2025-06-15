from django.db import models
from django.conf import settings
from enum import Enum

from apps.book.domain.entities import (
    UserBook,
    UserBookStatus,
    ReadingLog,
    Memo,
)


class UserBookModel(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 책 정보 (사용자가 직접 입력)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    total_pages = models.PositiveIntegerField()
    
    # 선택적 책 정보
    publisher = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    
    # 독서 상태
    status = models.CharField(
        max_length=20, choices=[(s.name, s.value) for s in UserBookStatus]
    )
    current_page = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_books"
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["title", "author"]),
        ]

    def to_domain(self) -> UserBook:
        return UserBook(
            id=self.id,
            user_id=str(self.user_id),
            title=self.title,
            author=self.author,
            total_pages=self.total_pages,
            publisher=self.publisher,
            isbn=self.isbn,
            cover_image_url=self.cover_image_url,
            status=UserBookStatus[self.status],
            current_page=self.current_page,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_domain(entity: UserBook) -> "UserBookModel":
        return UserBookModel(
            id=entity.id,
            user_id=entity.user_id,
            title=entity.title,
            author=entity.author,
            total_pages=entity.total_pages,
            publisher=entity.publisher,
            isbn=entity.isbn,
            cover_image_url=entity.cover_image_url,
            status=entity.status.name,
            current_page=entity.current_page,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class ReadingLogModel(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user_book = models.ForeignKey(UserBookModel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    start_page = models.PositiveIntegerField()
    end_page = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reading_logs"
        ordering = ["-date", "-created_at"]

    def to_domain(self) -> ReadingLog:
        return ReadingLog(
            id=self.id,
            user_book_id=str(self.user_book_id),
            user_id=str(self.user_id),
            date=self.date,
            start_page=self.start_page,
            end_page=self.end_page,
            note=self.note,
            created_at=self.created_at,
        )

    @staticmethod
    def from_domain(entity: ReadingLog) -> "ReadingLogModel":
        return ReadingLogModel(
            id=entity.id,
            user_book_id=entity.user_book_id,
            user_id=entity.user_id,
            date=entity.date,
            start_page=entity.start_page,
            end_page=entity.end_page,
            note=entity.note,
        )


class MemoModel(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user_book = models.ForeignKey(UserBookModel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    page = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "memos"
        ordering = ["-created_at"]

    def to_domain(self) -> Memo:
        return Memo(
            id=self.id,
            user_book_id=str(self.user_book_id),
            user_id=str(self.user_id),
            content=self.content,
            page=self.page,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_domain(entity: Memo) -> "MemoModel":
        return MemoModel(
            id=entity.id,
            user_book_id=entity.user_book_id,
            user_id=entity.user_id,
            content=entity.content,
            page=entity.page,
        )
