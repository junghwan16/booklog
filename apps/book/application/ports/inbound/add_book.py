from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from apps.book.domain.exceptions import InvalidBookDataError


@dataclass(frozen=True, slots=True)
class AddBookCommand:
    """Command to add a new book to user's library."""
    
    user_id: str
    title: str
    author: str
    total_pages: int
    publisher: Optional[str] = None
    isbn: Optional[str] = None
    cover_image_url: Optional[str] = None
    
    def __post_init__(self):
        """Validate command data after initialization."""
        # Strip whitespace and validate
        object.__setattr__(self, 'user_id', self.user_id.strip() if self.user_id else '')
        object.__setattr__(self, 'title', self.title.strip() if self.title else '')
        object.__setattr__(self, 'author', self.author.strip() if self.author else '')
        
        if not self.user_id:
            raise InvalidBookDataError("사용자 ID는 필수입니다.")
        
        if not self.title:
            raise InvalidBookDataError("제목은 필수입니다.")
        
        if not self.author:
            raise InvalidBookDataError("저자는 필수입니다.")
        
        if self.total_pages <= 0:
            raise InvalidBookDataError("총 페이지 수는 양수여야 합니다.")
        
        # Handle optional fields - strip and convert empty to None
        if self.publisher is not None:
            stripped_publisher = self.publisher.strip()
            object.__setattr__(self, 'publisher', stripped_publisher if stripped_publisher else None)
        
        if self.isbn is not None:
            stripped_isbn = self.isbn.strip()
            object.__setattr__(self, 'isbn', stripped_isbn if stripped_isbn else None)
        
        if self.cover_image_url is not None:
            stripped_url = self.cover_image_url.strip()
            object.__setattr__(self, 'cover_image_url', stripped_url if stripped_url else None)


class AddBookUseCase(ABC):
    """Interface for adding a book to user's library."""
    
    @abstractmethod
    def execute(self, cmd: AddBookCommand) -> str:
        """Execute add book use case and return book ID."""
        ... 