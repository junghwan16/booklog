from abc import ABC, abstractmethod


class SessionManagerPort(ABC):
    @abstractmethod
    def login(self, request, user_id: int): ...

    @abstractmethod
    def logout(self, request): ...
