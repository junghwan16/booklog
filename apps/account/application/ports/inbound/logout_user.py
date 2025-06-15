from abc import ABC, abstractmethod
from typing import Any


class LogoutUserUseCase(ABC):
    @abstractmethod
    def execute(self, request: Any) -> None: ...
