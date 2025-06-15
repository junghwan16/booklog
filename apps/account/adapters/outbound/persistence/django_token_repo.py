import secrets
from datetime import datetime
from .models import TokenModel
from apps.account.application.ports.outbound.token_repo import TokenRepository


class DjangoTokenRepository(TokenRepository):
    """Django ORM implementation using Django's default User model"""

    def issue(self, user_id: int, purpose: str, ttl_sec: int | None = None) -> str:
        token = secrets.token_urlsafe(32)
        TokenModel.create(
            user_id=user_id,
            token=token,
            purpose=purpose,
            ttl_sec=ttl_sec,
        )
        return token

    def consume(self, token: str, purpose: str) -> int | None:
        """Consume token and return user_id if valid"""
        try:
            obj = TokenModel.objects.get(token=token, purpose=purpose)
        except TokenModel.DoesNotExist:
            return None

        if obj.expires_at < datetime.now(obj.expires_at.tzinfo):
            return None

        user_id = obj.user_id
        obj.delete()
        return user_id
