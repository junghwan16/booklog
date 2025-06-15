from __future__ import annotations
from typing import Dict, Optional

from apps.account.application.ports.outbound.token_repo import TokenRepository


class FakeTokenRepository(TokenRepository):
    def __init__(self):
        self._tokens: Dict[str, int] = {}

    def issue(self, user_id: int, purpose: str, ttl_sec: int | None = None) -> str:
        token = f"token-for-{user_id}-with-purpose-{purpose}"
        self._tokens[token] = user_id
        return token

    def consume(self, token: str, purpose: str) -> Optional[int]:
        # purpose is ignored in this fake implementation
        return self._tokens.pop(token, None)
