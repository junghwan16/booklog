from apps.book.application.ports.inbound.add_memo import (
    AddMemoUseCase,
    AddMemoCommand,
)
from apps.book.application.ports.outbound.memo_repository import MemoRepository
from apps.book.application.ports.outbound.user_book_repository import UserBookRepository
from apps.book.domain.entities import Memo
from apps.book.domain.exceptions import (
    BookNotFoundError,
    UnauthorizedBookAccessError,
    InvalidMemoDataError,
)


class AddMemoService(AddMemoUseCase):
    def __init__(self, memo_repo: MemoRepository, user_book_repo: UserBookRepository):
        self._memo_repo = memo_repo
        self._user_book_repo = user_book_repo

    def execute(self, cmd: AddMemoCommand) -> str:
        # Command validation is handled in __post_init__

        # 비즈니스 검증: 책이 존재하고 사용자 소유인지 확인
        user_book = self._user_book_repo.get_by_id(cmd.book_id)
        if not user_book:
            raise BookNotFoundError(cmd.book_id)

        if user_book.user_id != cmd.user_id:
            raise UnauthorizedBookAccessError(cmd.user_id, cmd.book_id)

        # 비즈니스 검증: 페이지 번호가 총 페이지를 초과할 수 없음
        if cmd.page_number > user_book.total_pages:
            raise InvalidMemoDataError(
                "페이지 번호가 총 페이지 수를 초과할 수 없습니다."
            )

        memo = Memo(
            user_id=cmd.user_id,
            book_id=cmd.book_id,
            content=cmd.content.strip(),
            page_number=cmd.page_number,
        )

        saved_memo = self._memo_repo.save(memo)
        return saved_memo.id
