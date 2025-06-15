"""
이 파일은 애플리케이션 서비스와 그 의존성을 구성하는 중앙 지점(Composition Root) 역할을 합니다.
모든 리포지토리와 외부 서비스의 구체적인 구현은 여기서 한 번만 참조됩니다.
"""

from apps.account.adapters.outbound.persistence.django_user_repo import (
    DjangoUserRepository,
)
from apps.account.adapters.outbound.persistence.django_token_repo import (
    DjangoTokenRepository,
)
from apps.account.adapters.outbound.security.django_session_manager import (
    DjangoSessionManager,
)
from apps.account.adapters.outbound.email.django_email_sender import DjangoEmailSender

from .services.register_user_service import RegisterUserService
from .services.auth_service import AuthenticateUserService, LogoutUserService
from .services.password_service import (
    ChangePasswordService,
    RequestPasswordResetService,
    ResetPasswordService,
)

# Outbound Port Implementations (Adapters)
_user_repo = DjangoUserRepository()
_token_repo = DjangoTokenRepository()
_session_manager = DjangoSessionManager()
_email_sender = DjangoEmailSender()


# Application Services (Use Cases)
register_user_service = RegisterUserService(
    user_repo=_user_repo,
    email_sender=_email_sender,
    token_repo=_token_repo,
)

auth_service = AuthenticateUserService(
    session_manager=_session_manager,
)

logout_service = LogoutUserService(
    session_manager=_session_manager,
)

change_password_service = ChangePasswordService(
    user_repo=_user_repo,
)

request_password_reset_service = RequestPasswordResetService(
    user_repo=_user_repo,
    token_repo=_token_repo,
    email_sender=_email_sender,
)

reset_password_service = ResetPasswordService(
    user_repo=_user_repo,
    token_repo=_token_repo,
)
