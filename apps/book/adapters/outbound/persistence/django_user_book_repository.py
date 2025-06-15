from typing import List, Optional
from uuid import uuid4

from apps.book.application.ports.outbound.user_book_repository import UserBookRepository
from apps.book.domain.entities import UserBook, UserBookStatus
from .models import UserBookModel


class DjangoUserBookRepository(UserBookRepository):
    def save(self, user_book: UserBook) -> UserBook:
        if user_book.id:
            # Update existing book
            try:
                model = UserBookModel.objects.get(id=user_book.id)
                model = UserBookModel.from_domain(user_book)
                model.save()
            except UserBookModel.DoesNotExist:
                raise ValueError("책을 찾을 수 없습니다.")
        else:
            # Create new book
            user_book.id = str(uuid4())
            model = UserBookModel.from_domain(user_book)
            model.save()

        return UserBookModel.objects.get(id=model.id).to_domain()

    def get_by_id(self, user_book_id: str) -> Optional[UserBook]:
        try:
            model = UserBookModel.objects.get(id=user_book_id)
            return model.to_domain()
        except UserBookModel.DoesNotExist:
            return None

    def get_all_for_user(self, user_id: str) -> List[UserBook]:
        models = UserBookModel.objects.filter(user_id=user_id).order_by("-created_at")
        return [model.to_domain() for model in models]

    def get_by_user_id_and_status(
        self, user_id: str, status: UserBookStatus
    ) -> List[UserBook]:
        models = UserBookModel.objects.filter(user_id=user_id, status=status.name)
        return [model.to_domain() for model in models]

    def delete(self, user_book_id: str) -> None:
        try:
            UserBookModel.objects.get(id=user_book_id).delete()
        except UserBookModel.DoesNotExist:
            pass
