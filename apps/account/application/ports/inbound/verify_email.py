from abc import ABC, abstractmethod


class VerifyEmailUseCase(ABC):
    @abstractmethod
    def execute(self, token: str) -> None: ...
