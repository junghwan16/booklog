from abc import ABC, abstractmethod
from dataclasses import dataclass
from django.http import HttpRequest


@dataclass(slots=True)
class AuthenticateUserCommand:
    email: str
    password: str


class AuthenticateUserUseCase(ABC):
    @abstractmethod
    def execute(self, cmd: AuthenticateUserCommand, request: HttpRequest) -> None: ...
