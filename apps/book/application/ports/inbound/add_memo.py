from abc import ABC, abstractmethod
from dataclasses import dataclass
from apps.book.domain.exceptions import InvalidMemoDataError


@dataclass(frozen=True, slots=True)
class AddMemoCommand:
    """Command to add a memo for a book."""

    user_id: str
    book_id: str
    content: str
    page_number: int

    def __post_init__(self):
        """Validate command data after initialization."""
        if not self.user_id or not self.user_id.strip():
            raise InvalidMemoDataError("사용자 ID는 필수입니다.")

        if not self.book_id or not self.book_id.strip():
            raise InvalidMemoDataError("책 ID는 필수입니다.")

        if not self.content or not self.content.strip():
            raise InvalidMemoDataError("메모 내용은 필수입니다.")

        if self.page_number < 0:
            raise InvalidMemoDataError("페이지 번호는 0 이상이어야 합니다.")


class AddMemoUseCase(ABC):
    """Interface for adding a memo to a book."""

    @abstractmethod
    def execute(self, cmd: AddMemoCommand) -> str:
        """Execute add memo use case and return memo ID."""
        ...
