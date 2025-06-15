import unittest
from unittest.mock import MagicMock
from datetime import date, timedelta

from apps.book.domain.entities import UserBook, BookInfo, ReadingLog, UserBookStatus
from apps.book.application.services.dashboard_service import DashboardService


class DashboardServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_book_repo = MagicMock()
        self.reading_log_repo = MagicMock()
        self.dashboard_service = DashboardService(
            user_book_repo=self.user_book_repo, reading_log_repo=self.reading_log_repo
        )
        self.user_id = "user1"
        self.book_info = BookInfo(
            title="Test Book", author="Test Author", page_count=300
        )

    def test_get_dashboard_data_returns_correct_stats(self):
        # Arrange: Mock 리포지토리 설정
        self.user_book_repo.get_by_user_id_and_status.side_effect = [
            [UserBook(user_id=self.user_id, book_info=self.book_info)],  # TO_READ
            [],  # READING
            [UserBook(user_id=self.user_id, book_info=self.book_info)],  # FINISHED
        ]

        # Act
        data = self.dashboard_service.get_dashboard_data(self.user_id)

        # Assert
        stats = data["stats"]
        self.assertEqual(stats["to_read_count"], 1)
        self.assertEqual(stats["reading_count"], 0)
        self.assertEqual(stats["finished_count"], 1)
        self.assertEqual(stats["total_books"], 2)

    def test_get_reading_calendar_data_creates_correct_lawn(self):
        # Arrange
        today = date.today()
        yesterday = today - timedelta(days=1)

        logs = [
            ReadingLog(
                user_book_id="ub1",
                user_id=self.user_id,
                date=today,
                start_page=0,
                end_page=20,
            ),
            ReadingLog(
                user_book_id="ub1",
                user_id=self.user_id,
                date=today,
                start_page=20,
                end_page=30,
            ),
            ReadingLog(
                user_book_id="ub2",
                user_id=self.user_id,
                date=yesterday,
                start_page=10,
                end_page=25,
            ),
        ]
        self.reading_log_repo.get_by_user_id_and_date_range.return_value = logs

        # Act
        data = self.dashboard_service.get_reading_calendar_data(self.user_id)
        calendar_data = data["calendar_data"]

        # Assert: 365일치 데이터가 생성되었는지 확인
        self.assertEqual(len(calendar_data), 365)

        today_data = next(d for d in calendar_data if d["date"] == today.isoformat())
        yesterday_data = next(
            d for d in calendar_data if d["date"] == yesterday.isoformat()
        )

        self.assertEqual(today_data["pages"], 30)  # 20 + 10
        self.assertEqual(today_data["level"], 3)  # 30 // 10 = 3

        self.assertEqual(yesterday_data["pages"], 15)  # 25 - 10
        self.assertEqual(yesterday_data["level"], 1)  # 15 // 10 = 1


if __name__ == "__main__":
    unittest.main()
