from __future__ import annotations
from datetime import date, timedelta
from collections import defaultdict
from typing import Dict, Any

from apps.book.domain.entities import UserBookStatus
from ..ports.outbound.user_book_repository import UserBookRepository
from ..ports.outbound.reading_log_repository import ReadingLogRepository


class DashboardService:
    def __init__(
        self, user_book_repo: UserBookRepository, reading_log_repo: ReadingLogRepository
    ):
        self._user_book_repo = user_book_repo
        self._reading_log_repo = reading_log_repo

    def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        to_read = self._user_book_repo.get_by_user_id_and_status(
            user_id, UserBookStatus.TO_READ
        )
        reading = self._user_book_repo.get_by_user_id_and_status(
            user_id, UserBookStatus.READING
        )
        finished = self._user_book_repo.get_by_user_id_and_status(
            user_id, UserBookStatus.FINISHED
        )

        return {
            "stats": {
                "to_read_count": len(to_read),
                "reading_count": len(reading),
                "finished_count": len(finished),
                "total_books": len(to_read) + len(reading) + len(finished),
            }
        }

    def get_reading_calendar_data(self, user_id: str) -> Dict[str, Any]:
        today = date.today()
        start_date = today - timedelta(days=364)
        logs = self._reading_log_repo.get_by_user_id_and_date_range(
            user_id, start_date, today
        )

        daily_stats = defaultdict(lambda: {"pages": 0})
        for log in logs:
            daily_stats[log.date]["pages"] += log.pages_read

        calendar_data = []
        current_date = start_date
        while current_date <= today:
            stats = daily_stats[current_date]
            calendar_data.append(
                {
                    "date": current_date.isoformat(),
                    "pages": stats["pages"],
                    "level": min(stats["pages"] // 10, 4),  # 0-4 level
                }
            )
            current_date += timedelta(days=1)

        return {
            "calendar_data": calendar_data,
            "year": today.year,
        }
