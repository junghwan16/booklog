from abc import ABC, abstractmethod


class TokenRepository(ABC):
    @abstractmethod
    def issue(
        self, user_id: int, *, purpose: str, ttl_sec: int | None = None
    ) -> str: ...
    @abstractmethod
    def consume(self, token: str, *, purpose: str) -> int | None: ...
