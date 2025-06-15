from apps.account.application.ports.inbound.authenticate_user import (
    AuthenticateUserUseCase,
    AuthenticateUserCommand,
)
from apps.account.application.ports.inbound.logout_user import LogoutUserUseCase
from apps.account.application.ports.outbound.authenticator import AuthenticatorPort
from apps.account.application.ports.outbound.session_manager import SessionManagerPort
from apps.account.domain.exceptions import InvalidCredentials
from apps.account.domain.models import Account


class AuthenticateUserService(AuthenticateUserUseCase):
    def __init__(self, authenticator: AuthenticatorPort):
        self.authenticator = authenticator

    def execute(self, cmd: AuthenticateUserCommand) -> Account:
        account = self.authenticator.authenticate(
            email=cmd.email, password=cmd.password
        )

        if account is None:
            raise InvalidCredentials()

        return account


class LogoutUserService(LogoutUserUseCase):
    def __init__(self, session_manager: SessionManagerPort):
        self.session_manager = session_manager

    def execute(self, request) -> None:
        self.session_manager.logout(request)
