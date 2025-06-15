from apps.account.application.ports.inbound.delete_account import DeleteAccountUseCase
from apps.account.application.ports.outbound import user_repo


class DeleteAccountService(DeleteAccountUseCase):
    def __init__(self, user_repo: user_repo.UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> None:
        self.user_repo.delete(user_id)
