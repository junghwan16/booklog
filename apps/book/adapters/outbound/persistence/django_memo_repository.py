from typing import List, Optional
from uuid import uuid4

from apps.book.application.ports.outbound.memo_repository import MemoRepository
from apps.book.domain.entities import Memo
from apps.book.models import MemoModel


class DjangoMemoRepository(MemoRepository):
    def save(self, memo: Memo) -> Memo:
        if memo.id:
            # Update existing memo
            try:
                memo_model = MemoModel.objects.get(id=memo.id)
                memo_model.content = memo.content
                memo_model.page_number = memo.page_number
                memo_model.save()
            except MemoModel.DoesNotExist:
                raise ValueError("메모를 찾을 수 없습니다.")
        else:
            # Create new memo
            memo.id = str(uuid4())
            memo_model = MemoModel.objects.create(
                id=memo.id,
                user_id=memo.user_id,
                book_id=memo.book_id,
                content=memo.content,
                page_number=memo.page_number,
            )
        
        return self._to_entity(memo_model)

    def get_by_id(self, memo_id: str) -> Optional[Memo]:
        try:
            memo_model = MemoModel.objects.get(id=memo_id)
            return self._to_entity(memo_model)
        except MemoModel.DoesNotExist:
            return None

    def get_by_book_id(self, book_id: str) -> List[Memo]:
        memo_models = MemoModel.objects.filter(book_id=book_id).order_by('page_number', 'created_at')
        return [self._to_entity(model) for model in memo_models]

    def delete(self, memo_id: str) -> None:
        MemoModel.objects.filter(id=memo_id).delete()

    def _to_entity(self, model: MemoModel) -> Memo:
        return Memo(
            id=model.id,
            user_id=model.user_id,
            book_id=model.book_id,
            content=model.content,
            page_number=model.page_number,
            created_at=model.created_at,
        ) 