"""Domain exceptions for the book module."""


class BookDomainError(Exception):
    """Base exception for book domain errors."""

    pass


class BookNotFoundError(BookDomainError):
    """Raised when a book is not found."""

    def __init__(self, book_id: str):
        self.book_id = book_id
        super().__init__(f"Book with ID {book_id} not found")


class UnauthorizedBookAccessError(BookDomainError):
    """Raised when user tries to access a book they don't own."""

    def __init__(self, user_id: str, book_id: str):
        self.user_id = user_id
        self.book_id = book_id
        super().__init__(f"User {user_id} is not authorized to access book {book_id}")


class InvalidBookDataError(BookDomainError):
    """Raised when book data is invalid."""

    pass


class InvalidProgressError(BookDomainError):
    """Raised when reading progress is invalid."""

    pass


class MemoNotFoundError(BookDomainError):
    """Raised when a memo is not found."""

    def __init__(self, memo_id: str):
        self.memo_id = memo_id
        super().__init__(f"Memo with ID {memo_id} not found")


class InvalidMemoDataError(BookDomainError):
    """Raised when memo data is invalid."""

    pass
