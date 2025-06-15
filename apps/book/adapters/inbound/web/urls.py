from django.urls import path
from . import views

app_name = "book"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("library/", views.library_view, name="library"),
    path("add-book/", views.add_book_view, name="add_book"),
    path("start-reading/", views.start_reading_view, name="start_reading"),
    path("update-progress/", views.update_progress_view, name="update_progress"),
]
