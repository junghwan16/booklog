from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class ResetPasswordCommand:
    token: str
    new_password: str


class ResetPasswordUseCase(ABC):
    @abstractmethod
    def execute(self, cmd: ResetPasswordCommand) -> None: ...
