from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.account.domain.models import Account, AccountStatus
from django.contrib.auth.models import AbstractUser


class AccountModel(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def to_domain(self) -> Account:
        return Account(
            id=self.id,
            email=self.email,
            nickname=self.username,
            is_email_verified=self.is_email_verified,
            status=AccountStatus.ACTIVE if self.is_active else AccountStatus.DELETED,
        )


class TokenModel(models.Model):
    PURPOSE_EMAIL_VERIFY = "email_verify"
    PURPOSE_PWD_RESET = "pwd_reset"

    PURPOSE_CHOICES = [
        (PURPOSE_EMAIL_VERIFY, "Email Verify"),
        (PURPOSE_PWD_RESET, "Password Reset"),
    ]

    token = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=32, choices=PURPOSE_CHOICES)
    expires_at = models.DateTimeField()

    @classmethod
    def create(cls, *, user_id: int, token: str, purpose: str, ttl_sec: int | None):
        exp = timezone.now() + timedelta(seconds=ttl_sec or 7 * 24 * 3600)
        return cls.objects.create(
            token=token, user_id=user_id, purpose=purpose, expires_at=exp
        )
