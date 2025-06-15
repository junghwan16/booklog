from apps.book.application.ports.inbound.add_book import (
    AddBookUseCase,
    AddBookCommand,
)
from apps.book.application.ports.outbound.user_book_repository import UserBookRepository
from apps.book.domain.entities import UserBook


class AddBookService(AddBookUseCase):
    def __init__(self, user_book_repo: UserBookRepository):
        self._user_book_repo = user_book_repo

    def execute(self, cmd: AddBookCommand) -> str:
        # Command validation and data cleaning is handled in __post_init__
        # Only business logic here
        user_book = UserBook(
            user_id=cmd.user_id,
            title=cmd.title,
            author=cmd.author,
            total_pages=cmd.total_pages,
            publisher=cmd.publisher,
            isbn=cmd.isbn,
            cover_image_url=cmd.cover_image_url,
        )
        
        saved_book = self._user_book_repo.save(user_book)
        return saved_book.id 