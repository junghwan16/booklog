from apps.account.application.ports.inbound.change_password import (
    ChangePasswordUseCase,
    ChangePasswordCommand,
)
from apps.account.application.ports.inbound.request_password_reset import (
    RequestPasswordResetUseCase,
    RequestPasswordResetCommand,
)
from apps.account.application.ports.inbound.reset_password import (
    ResetPasswordUseCase,
    ResetPasswordCommand,
)
from apps.account.application.ports.outbound import (
    user_repo,
    email_sender,
    token_repo,
)
from apps.account.domain.exceptions import InvalidCredentials, InvalidTokenError


class ChangePasswordService(ChangePasswordUseCase):
    def __init__(self, user_repo: user_repo.UserRepository):
        self.user_repo = user_repo

    def execute(self, cmd: ChangePasswordCommand) -> None:
        if not self.user_repo.check_password(cmd.user_id, cmd.old_password):
            raise InvalidCredentials()
        self.user_repo.change_password(cmd.user_id, cmd.new_password)


class RequestPasswordResetService(RequestPasswordResetUseCase):
    def __init__(
        self,
        user_repo: user_repo.UserRepository,
        token_repo: token_repo.TokenRepository,
        email_sender: email_sender.EmailSenderPort,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.email_sender = email_sender

    def execute(self, cmd: RequestPasswordResetCommand) -> None:
        acc = self.user_repo.find_by_email(cmd.email)
        if acc is None:
            return
        if acc.id is None:
            # Should not happen for an existing account
            return
        token = self.token_repo.issue(acc.id, purpose="pwd_reset", ttl_sec=60 * 60)
        self.email_sender.send_password_reset(acc.email, token)


class ResetPasswordService(ResetPasswordUseCase):
    def __init__(
        self,
        user_repo: user_repo.UserRepository,
        token_repo: token_repo.TokenRepository,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def execute(self, cmd: ResetPasswordCommand) -> None:
        user_id = self.token_repo.consume(cmd.token, purpose="pwd_reset")
        if user_id is None:
            raise InvalidTokenError()

        # Check if user exists before changing password
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise InvalidTokenError()

        self.user_repo.change_password(user_id, cmd.new_password)
