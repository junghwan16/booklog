from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from apps.account.application.ports.outbound.email_sender import EmailSenderPort


class DjangoEmailSender(EmailSenderPort):
    def _build_absolute_url(self, path: str) -> str:
        """상대 경로를 절대 URL로 변환합니다."""
        base_url = getattr(settings, "SITE_URL", "http://localhost:8000")
        return f"{base_url.rstrip('/')}{path}"

    def send_email_verify(self, to_email: str, token: str) -> None:
        verify_path = reverse("account:verify", kwargs={"token": token})
        verify_url = self._build_absolute_url(verify_path)

        send_mail(
            subject="BookLog 이메일 인증",
            message=f"BookLog 회원가입을 완료하기 위해 아래 링크를 클릭해 주세요:\n\n{verify_url}\n\n이 링크는 24시간 후 만료됩니다.",
            from_email="noreply@booklog.com",
            recipient_list=[to_email],
        )

    def send_password_reset(self, to_email: str, uid: str, token: str) -> None:
        uidb64 = urlsafe_base64_encode(force_bytes(uid))
        reset_path = reverse(
            "account:password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        reset_url = self._build_absolute_url(reset_path)

        send_mail(
            subject="BookLog 비밀번호 재설정",
            message=f"비밀번호를 재설정하려면 아래 링크를 클릭해 주세요:\n\n{reset_url}\n\n이 링크는 24시간 후 만료됩니다.",
            from_email="noreply@booklog.com",
            recipient_list=[to_email],
        )
