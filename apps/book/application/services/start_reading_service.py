from apps.book.application.ports.inbound.start_reading import (
    StartReadingUseCase,
    StartReadingCommand,
)
from apps.book.application.ports.outbound.user_book_repository import UserBookRepository
from apps.book.domain.exceptions import (
    BookNotFoundError,
    UnauthorizedBookAccessError,
)


class StartReadingService(StartReadingUseCase):
    def __init__(self, user_book_repo: UserBookRepository):
        self._user_book_repo = user_book_repo

    def execute(self, cmd: StartReadingCommand) -> None:
        # Command validation is handled in __post_init__
        
        user_book = self._user_book_repo.get_by_id(cmd.book_id)
        if not user_book:
            raise BookNotFoundError(cmd.book_id)
        
        if user_book.user_id != cmd.user_id:
            raise UnauthorizedBookAccessError(cmd.user_id, cmd.book_id)

        user_book.start_reading()
        self._user_book_repo.save(user_book) 