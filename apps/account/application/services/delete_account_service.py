from apps.account.application.ports.inbound.delete_account import DeleteAccountUseCase
from apps.account.application.ports.outbound import user_repo, session_manager
from django.http import HttpRequest


class DeleteAccountService(DeleteAccountUseCase):
    def __init__(
        self,
        user_repo: user_repo.UserRepository,
        session_manager: session_manager.SessionManagerPort,
    ):
        self.user_repo = user_repo
        self.session_manager = session_manager

    def execute(self, user_id: int, request: HttpRequest | None = None) -> None:
        self.user_repo.delete(user_id)
        if request is not None:
            self.session_manager.logout(request)
