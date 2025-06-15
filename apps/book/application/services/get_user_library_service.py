from typing import List
from apps.book.application.ports.inbound.get_user_library import (
    GetUserLibraryUseCase,
    GetUserLibraryQuery,
)
from apps.book.application.ports.outbound.user_book_repository import UserBookRepository
from apps.book.domain.entities import UserBook


class GetUserLibraryService(GetUserLibraryUseCase):
    def __init__(self, user_book_repo: UserBookRepository):
        self._user_book_repo = user_book_repo

    def execute(self, query: GetUserLibraryQuery) -> List[UserBook]:
        return self._user_book_repo.get_all_for_user(query.user_id)
