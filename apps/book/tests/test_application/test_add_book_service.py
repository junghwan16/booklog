import pytest
from unittest.mock import Mock
from uuid import uuid4

from apps.book.domain.entities import UserBook
from apps.book.domain.exceptions import InvalidBookDataError
from apps.book.application.services.add_book_service import AddBookService
from apps.book.application.ports.inbound.add_book import AddBookCommand


@pytest.fixture
def mock_user_book_repo():
    return Mock()


@pytest.fixture
def add_book_service(mock_user_book_repo):
    return AddBookService(user_book_repo=mock_user_book_repo)


def test_add_book_success(add_book_service, mock_user_book_repo):
    user_id = str(uuid4())
    book_id = str(uuid4())
    
    # Mock repository to return saved book with ID
    def save_side_effect(user_book):
        user_book.id = book_id
        return user_book
    mock_user_book_repo.save.side_effect = save_side_effect

    cmd = AddBookCommand(
        user_id=user_id,
        title="Test Book",
        author="Test Author",
        total_pages=300,
        publisher="Test Publisher",
        isbn="123456789"
    )

    result_book_id = add_book_service.execute(cmd)

    assert result_book_id == book_id
    mock_user_book_repo.save.assert_called_once()
    
    # Verify the saved book has correct properties
    saved_book = mock_user_book_repo.save.call_args[0][0]
    assert saved_book.user_id == user_id
    assert saved_book.title == "Test Book"
    assert saved_book.author == "Test Author"
    assert saved_book.total_pages == 300
    assert saved_book.publisher == "Test Publisher"
    assert saved_book.isbn == "123456789"


def test_add_book_empty_title_raises_error(add_book_service):
    with pytest.raises(InvalidBookDataError, match="제목은 필수입니다"):
        AddBookCommand(
            user_id=str(uuid4()),
            title="",
            author="Test Author",
            total_pages=300
        )


def test_add_book_empty_author_raises_error(add_book_service):
    with pytest.raises(InvalidBookDataError, match="저자는 필수입니다"):
        AddBookCommand(
            user_id=str(uuid4()),
            title="Test Book",
            author="",
            total_pages=300
        )


def test_add_book_invalid_total_pages_raises_error(add_book_service):
    with pytest.raises(InvalidBookDataError, match="총 페이지 수는 양수여야 합니다"):
        AddBookCommand(
            user_id=str(uuid4()),
            title="Test Book",
            author="Test Author",
            total_pages=0
        )


def test_add_book_strips_whitespace(add_book_service, mock_user_book_repo):
    user_id = str(uuid4())
    book_id = str(uuid4())
    
    def save_side_effect(user_book):
        user_book.id = book_id
        return user_book
    mock_user_book_repo.save.side_effect = save_side_effect

    cmd = AddBookCommand(
        user_id=user_id,
        title="  Test Book  ",
        author="  Test Author  ",
        total_pages=300,
        publisher="  Test Publisher  ",
        isbn="  123456789  "
    )

    add_book_service.execute(cmd)

    saved_book = mock_user_book_repo.save.call_args[0][0]
    assert saved_book.title == "Test Book"
    assert saved_book.author == "Test Author"
    assert saved_book.publisher == "Test Publisher"
    assert saved_book.isbn == "123456789" 