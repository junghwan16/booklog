from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.views.decorators.http import require_POST
from django.contrib import messages

from apps.book.application.services.dashboard_service import DashboardService
from apps.book.application.services.add_book_service import AddBookService
from apps.book.application.services.start_reading_service import StartReadingService
from apps.book.application.services.update_reading_progress_service import (
    UpdateReadingProgressService,
)
from apps.book.application.services.get_user_library_service import (
    GetUserLibraryService,
)

from apps.book.application.ports.inbound.add_book import AddBookCommand
from apps.book.application.ports.inbound.start_reading import StartReadingCommand
from apps.book.application.ports.inbound.update_reading_progress import (
    UpdateReadingProgressCommand,
)
from apps.book.application.ports.inbound.get_user_library import GetUserLibraryQuery

from apps.book.adapters.inbound.web.forms import (
    AddBookForm,
    StartReadingForm,
    UpdateProgressForm,
)

from apps.book.domain.exceptions import (
    BookDomainError,
    BookNotFoundError,
    UnauthorizedBookAccessError,
    InvalidBookDataError,
    InvalidProgressError,
)

from apps.book.adapters.outbound.persistence.django_user_book_repository import (
    DjangoUserBookRepository,
)
from apps.book.adapters.outbound.persistence.django_reading_log_repository import (
    DjangoReadingLogRepository,
)


def get_dashboard_service() -> DashboardService:
    return DashboardService(
        user_book_repo=DjangoUserBookRepository(),
        reading_log_repo=DjangoReadingLogRepository(),
    )


def get_add_book_service() -> AddBookService:
    return AddBookService(user_book_repo=DjangoUserBookRepository())


def get_start_reading_service() -> StartReadingService:
    return StartReadingService(user_book_repo=DjangoUserBookRepository())


def get_update_reading_progress_service() -> UpdateReadingProgressService:
    return UpdateReadingProgressService(user_book_repo=DjangoUserBookRepository())


def get_user_library_service() -> GetUserLibraryService:
    return GetUserLibraryService(user_book_repo=DjangoUserBookRepository())


@login_required
def dashboard_view(request: HttpRequest):
    """
    사용자 대시보드: 독서 통계 및 '독서 잔디' 표시
    """
    service = get_dashboard_service()
    user_id = str(request.user.id)

    context = service.get_dashboard_data(user_id)
    calendar_context = service.get_reading_calendar_data(user_id)
    context.update(calendar_context)

    return render(request, "book/dashboard.html", context)


@login_required
def add_book_view(request: HttpRequest):
    """
    새 책 추가 폼
    """
    if request.method == "POST":
        form = AddBookForm(request.POST)
        if form.is_valid():
            try:
                cmd = AddBookCommand(
                    user_id=str(request.user.id),
                    title=form.cleaned_data["title"],
                    author=form.cleaned_data["author"],
                    total_pages=form.cleaned_data["total_pages"],
                    publisher=form.cleaned_data.get("publisher") or None,
                    isbn=form.cleaned_data.get("isbn") or None,
                )

                service = get_add_book_service()
                book_id = service.execute(cmd)
                messages.success(
                    request,
                    f'"{form.cleaned_data["title"]}" 책이 서재에 추가되었습니다.',
                )
                return redirect("book:library")

            except BookDomainError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"책 추가 중 오류가 발생했습니다: {str(e)}")
        else:
            # Form validation errors will be displayed in template
            pass
    else:
        form = AddBookForm()

    return render(request, "book/add_book.html", {"form": form})


@login_required
def library_view(request: HttpRequest):
    """
    내 서재 - 사용자의 모든 책 목록
    """
    query = GetUserLibraryQuery(user_id=str(request.user.id))
    service = get_user_library_service()
    user_books = service.execute(query)

    # 상태별로 분류
    to_read_books = [book for book in user_books if book.status.name == "TO_READ"]
    reading_books = [book for book in user_books if book.status.name == "READING"]
    finished_books = [book for book in user_books if book.status.name == "FINISHED"]

    context = {
        "to_read_books": to_read_books,
        "reading_books": reading_books,
        "finished_books": finished_books,
        "total_books": len(user_books),
    }
    return render(request, "book/library.html", context)


@login_required
@require_POST
def start_reading_view(request: HttpRequest):
    """
    읽기 시작
    """
    form = StartReadingForm(request.POST)
    if form.is_valid():
        try:
            cmd = StartReadingCommand(
                user_id=str(request.user.id), book_id=form.cleaned_data["book_id"]
            )

            service = get_start_reading_service()
            service.execute(cmd)
            messages.success(request, "읽기를 시작했습니다.")

        except BookDomainError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"오류가 발생했습니다: {str(e)}")
    else:
        messages.error(request, "잘못된 요청입니다.")

    return redirect("book:library")


@login_required
@require_POST
def update_progress_view(request: HttpRequest):
    """
    읽기 진행도 업데이트
    """
    form = UpdateProgressForm(request.POST)
    if form.is_valid():
        try:
            cmd = UpdateReadingProgressCommand(
                user_id=str(request.user.id),
                book_id=form.cleaned_data["book_id"],
                current_page=form.cleaned_data["current_page"],
            )

            service = get_update_reading_progress_service()
            service.execute(cmd)
            messages.success(request, "진행도가 업데이트되었습니다.")

        except BookDomainError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"오류가 발생했습니다: {str(e)}")
    else:
        messages.error(request, "잘못된 요청입니다.")

    return redirect("book:library")
