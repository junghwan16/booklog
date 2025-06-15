from abc import ABC, abstractmethod


class DeleteAccountUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: int) -> None: ...
