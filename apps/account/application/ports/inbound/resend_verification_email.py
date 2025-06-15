from __future__ import annotations
from abc import ABC, abstractmethod


class ResendVerificationEmailUseCase(ABC):
    @abstractmethod
    def execute(self, email: str) -> None:
        raise NotImplementedError
