from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class ChangePasswordCommand:
    user_id: int
    old_password: str
    new_password: str


class ChangePasswordUseCase(ABC):
    @abstractmethod
    def execute(self, cmd: ChangePasswordCommand) -> None: ...
