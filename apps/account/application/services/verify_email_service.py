from apps.account.application.ports.inbound.verify_email import VerifyEmailUseCase
from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.application.ports.outbound.token_repo import TokenRepository
from apps.account.domain.exceptions import InvalidTokenError
from dataclasses import replace


class VerifyEmailService(VerifyEmailUseCase):
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def execute(self, token: str) -> None:
        user_id = self.token_repo.consume(token, purpose="email_verify")
        if user_id is None:
            raise InvalidTokenError()

        account = self.user_repo.find_by_id(user_id)
        if account is None:
            raise InvalidTokenError()

        if not account.is_email_verified:
            self.user_repo.save(replace(account, is_email_verified=True))
