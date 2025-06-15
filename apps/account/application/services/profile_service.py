from apps.account.application.ports.inbound.get_profile import GetProfileUseCase
from apps.account.application.ports.inbound.update_profile import (
    UpdateProfileUseCase,
    UpdateProfileCommand,
)
from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.domain.exceptions import NotFoundError
from dataclasses import replace


class GetProfileService(GetProfileUseCase):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int):
        acc = self.user_repo.find_by_id(user_id)
        if acc is None:
            raise NotFoundError("account")
        return acc


class UpdateProfileService(UpdateProfileUseCase):
    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    def execute(self, cmd: UpdateProfileCommand) -> None:
        acc = self.user_repo.find_by_id(cmd.user_id)
        if acc is None:
            raise NotFoundError("account")

        updated = acc
        if cmd.nickname is not None:
            updated = replace(updated, nickname=cmd.nickname)

        self.user_repo.save(updated)
