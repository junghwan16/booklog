from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class RequestPasswordResetCommand:
    email: str


class RequestPasswordResetUseCase(ABC):
    @abstractmethod
    def execute(self, cmd: RequestPasswordResetCommand) -> None: ...
