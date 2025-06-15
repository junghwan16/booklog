from apps.account.application.ports.inbound.register_user import (
    RegisterUserUseCase,
    RegisterUserCommand,
)
from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.application.ports.outbound.email_sender import EmailSenderPort
from apps.account.application.ports.outbound.token_repo import TokenRepository
from apps.account.domain.models import Account
from apps.account.domain.exceptions import DuplicateEmailError


class RegisterUserService(RegisterUserUseCase):
    def __init__(
        self,
        user_repo: UserRepository,
        email_sender: EmailSenderPort,
        token_repo: TokenRepository,
    ):
        self.user_repo = user_repo
        self.email_sender = email_sender
        self.token_repo = token_repo

    def execute(self, cmd: RegisterUserCommand) -> int:
        if self.user_repo.exists_by_email(cmd.email):
            raise DuplicateEmailError(cmd.email)

        account = Account(
            id=None,
            email=cmd.email,
            nickname=cmd.nickname,
            password=cmd.password,
            is_email_verified=False,
        )
        new_id = self.user_repo.save(account)

        # 이메일 인증 토큰 발급 & 발송
        token = self.token_repo.issue(new_id, purpose="email_verify")
        self.email_sender.send_email_verify(cmd.email, token)
        return new_id
