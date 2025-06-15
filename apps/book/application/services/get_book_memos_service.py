from typing import List
from apps.book.application.ports.inbound.get_book_memos import (
    GetBookMemosUseCase,
    GetBookMemosQuery,
)
from apps.book.application.ports.outbound.memo_repository import MemoRepository
from apps.book.application.ports.outbound.user_book_repository import UserBookRepository
from apps.book.domain.entities import Memo


class GetBookMemosService(GetBookMemosUseCase):
    def __init__(self, memo_repo: MemoRepository, user_book_repo: UserBookRepository):
        self._memo_repo = memo_repo
        self._user_book_repo = user_book_repo

    def execute(self, query: GetBookMemosQuery) -> List[Memo]:
        # 비즈니스 검증: 책이 존재하고 사용자 소유인지 확인
        user_book = self._user_book_repo.get_by_id(query.book_id)
        if not user_book:
            raise ValueError("책을 찾을 수 없습니다.")
        
        if user_book.user_id != query.user_id:
            raise ValueError("권한이 없습니다.")

        return self._memo_repo.get_by_book_id(query.book_id) 