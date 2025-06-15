from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    """Command to register a new user."""

    email: str
    nickname: str
    password: str


class RegisterUserUseCase(ABC):
    """Interface for the user registration use-case."""

    @abstractmethod
    def execute(self, cmd: RegisterUserCommand) -> int: ...
