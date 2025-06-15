from typing import List, Optional
from datetime import date
from uuid import uuid4

from apps.book.application.ports.outbound.reading_log_repository import (
    ReadingLogRepository,
)
from apps.book.domain.entities import ReadingLog
from .models import ReadingLogModel


class DjangoReadingLogRepository(ReadingLogRepository):
    def save(self, reading_log: ReadingLog) -> ReadingLog:
        if reading_log.id:
            # Update existing log
            try:
                model = ReadingLogModel.objects.get(id=reading_log.id)
                model = ReadingLogModel.from_domain(reading_log)
                model.save()
            except ReadingLogModel.DoesNotExist:
                raise ValueError("독서 기록을 찾을 수 없습니다.")
        else:
            # Create new log
            reading_log.id = str(uuid4())
            model = ReadingLogModel.from_domain(reading_log)
            model.save()

        return ReadingLogModel.objects.get(id=model.id).to_domain()

    def get_by_id(self, reading_log_id: str) -> Optional[ReadingLog]:
        try:
            model = ReadingLogModel.objects.get(id=reading_log_id)
            return model.to_domain()
        except ReadingLogModel.DoesNotExist:
            return None

    def get_by_user_id_and_date_range(
        self, user_id: str, start_date: date, end_date: date
    ) -> List[ReadingLog]:
        models = ReadingLogModel.objects.filter(
            user_id=user_id, date__range=[start_date, end_date]
        ).order_by("-date", "-created_at")
        return [model.to_domain() for model in models]

    def get_by_user_book_id(self, user_book_id: str) -> List[ReadingLog]:
        models = ReadingLogModel.objects.filter(user_book_id=user_book_id).order_by(
            "-date", "-created_at"
        )
        return [model.to_domain() for model in models]

    def delete(self, reading_log_id: str) -> None:
        try:
            ReadingLogModel.objects.get(id=reading_log_id).delete()
        except ReadingLogModel.DoesNotExist:
            pass
