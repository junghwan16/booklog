from abc import ABC, abstractmethod
from dataclasses import dataclass
from apps.book.domain.exceptions import InvalidBookDataError


@dataclass(frozen=True, slots=True)
class StartReadingCommand:
    """Command to start reading a book."""

    user_id: str
    book_id: str

    def __post_init__(self):
        """Validate command data after initialization."""
        if not self.user_id or not self.user_id.strip():
            raise InvalidBookDataError("사용자 ID는 필수입니다.")

        if not self.book_id or not self.book_id.strip():
            raise InvalidBookDataError("책 ID는 필수입니다.")


class StartReadingUseCase(ABC):
    """Interface for starting to read a book."""

    @abstractmethod
    def execute(self, cmd: StartReadingCommand) -> None:
        """Execute start reading use case."""
        ...
