from __future__ import annotations

from apps.account.application.ports.inbound.resend_verification_email import (
    ResendVerificationEmailUseCase,
)
from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.application.ports.outbound.email_sender import EmailSenderPort
from apps.account.application.ports.outbound.token_repo import TokenRepository
from apps.account.domain.exceptions import UserNotFoundError


class ResendVerificationEmailService(ResendVerificationEmailUseCase):
    def __init__(
        self,
        user_repo: UserRepository,
        email_sender: EmailSenderPort,
        token_repo: TokenRepository,
    ):
        self.user_repo = user_repo
        self.email_sender = email_sender
        self.token_repo = token_repo

    def execute(self, email: str) -> None:
        account = self.user_repo.find_by_email(email)
        if account is None:
            raise UserNotFoundError()

        if account.is_email_verified:
            # 이미 인증된 유저는 아무것도 하지 않음
            return

        token = self.token_repo.issue(account.id, purpose="email_verify")
        self.email_sender.send_email_verify(email, token)
