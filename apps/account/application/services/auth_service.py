from django.contrib.auth import authenticate
from django.http import HttpRequest
from apps.account.application.ports.inbound.authenticate_user import (
    AuthenticateUserUseCase,
    AuthenticateUserCommand,
)
from apps.account.application.ports.inbound.logout_user import LogoutUserUseCase
from apps.account.application.ports.outbound.session_manager import SessionManagerPort
from apps.account.domain.exceptions import InvalidCredentials


class AuthenticateUserService(AuthenticateUserUseCase):
    def __init__(self, session_manager: SessionManagerPort):
        self.session_manager = session_manager

    def execute(self, cmd: AuthenticateUserCommand, request: HttpRequest) -> None:
        user = authenticate(request, username=cmd.email, password=cmd.password)

        if user is None:
            raise InvalidCredentials()

        self.session_manager.login(request, user.id)


class LogoutUserService(LogoutUserUseCase):
    def __init__(self, session_manager: SessionManagerPort):
        self.session_manager = session_manager

    def execute(self, request: HttpRequest) -> None:
        self.session_manager.logout(request)
