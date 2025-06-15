from abc import ABC, abstractmethod


class GetProfileUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: int):
        """반환값: 도메인 Account DTO"""
        ...
