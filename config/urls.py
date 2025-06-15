from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def home_redirect(request):
    """루트 URL을 대시보드로 리다이렉트"""
    if request.user.is_authenticated:
        return redirect("book:dashboard")
    else:
        return redirect("account:login")


urlpatterns = [
    path("", home_redirect, name="home"),
    path("admin/", admin.site.urls),
    path(
        "accounts/",
        include("apps.account.adapters.inbound.web.urls"),
    ),
    path("books/", include("apps.book.adapters.inbound.web.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
