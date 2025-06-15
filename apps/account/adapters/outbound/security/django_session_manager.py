from django.contrib.auth import login as _login, logout as _logout, get_user_model
from apps.account.application.ports.outbound.session_manager import SessionManagerPort

User = get_user_model()


class DjangoSessionManager(SessionManagerPort):
    def login(self, request, user_id: int):
        user = User.objects.get(id=user_id)
        _login(request, user)

    def logout(self, request):
        _logout(request)
