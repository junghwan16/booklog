from apps.book.application.ports.inbound.update_reading_progress import (
    UpdateReadingProgressUseCase,
    UpdateReadingProgressCommand,
)
from apps.book.application.ports.outbound.user_book_repository import UserBookRepository
from apps.book.domain.exceptions import (
    BookNotFoundError,
    UnauthorizedBookAccessError,
    InvalidProgressError,
)


class UpdateReadingProgressService(UpdateReadingProgressUseCase):
    def __init__(self, user_book_repo: UserBookRepository):
        self._user_book_repo = user_book_repo

    def execute(self, cmd: UpdateReadingProgressCommand) -> None:
        # Command validation is handled in __post_init__
        
        user_book = self._user_book_repo.get_by_id(cmd.book_id)
        if not user_book:
            raise BookNotFoundError(cmd.book_id)
        
        if user_book.user_id != cmd.user_id:
            raise UnauthorizedBookAccessError(cmd.user_id, cmd.book_id)

        # 비즈니스 검증: 현재 페이지가 총 페이지를 초과할 수 없음
        if cmd.current_page > user_book.total_pages:
            raise InvalidProgressError("현재 페이지가 총 페이지 수를 초과할 수 없습니다.")

        user_book.update_progress(cmd.current_page)
        self._user_book_repo.save(user_book) 