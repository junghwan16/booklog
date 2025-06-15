from abc import ABC, abstractmethod
from django.http import HttpRequest


class LogoutUserUseCase(ABC):
    @abstractmethod
    def execute(self, request: HttpRequest) -> None: ...
