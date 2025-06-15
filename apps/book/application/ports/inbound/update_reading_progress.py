from abc import ABC, abstractmethod
from dataclasses import dataclass
from apps.book.domain.exceptions import InvalidProgressError


@dataclass(frozen=True, slots=True)
class UpdateReadingProgressCommand:
    """Command to update reading progress."""

    user_id: str
    book_id: str
    current_page: int

    def __post_init__(self):
        """Validate command data after initialization."""
        if not self.user_id or not self.user_id.strip():
            raise InvalidProgressError("사용자 ID는 필수입니다.")

        if not self.book_id or not self.book_id.strip():
            raise InvalidProgressError("책 ID는 필수입니다.")

        if self.current_page < 0:
            raise InvalidProgressError("현재 페이지는 0 이상이어야 합니다.")


class UpdateReadingProgressUseCase(ABC):
    """Interface for updating reading progress."""

    @abstractmethod
    def execute(self, cmd: UpdateReadingProgressCommand) -> None:
        """Execute update reading progress use case."""
        ...
