from django.core.mail import send_mail
from apps.account.application.ports.outbound.email_sender import EmailSenderPort


class DjangoEmailSender(EmailSenderPort):
    def send_email_verify(self, to_email: str, token: str) -> None:
        send_mail(
            subject="이메일 인증 링크",
            message=f"이메일 인증 링크: http://localhost:8000/verify-email/{token}",
            from_email="noreply@example.com",
            recipient_list=[to_email],
        )

    def send_password_reset(self, to_email: str, token: str) -> None:
        send_mail(
            subject="비밀번호 재설정 링크",
            message=f"비밀번호 재설정 링크: http://localhost:8000/reset-password/{token}",
            from_email="noreply@example.com",
            recipient_list=[to_email],
        )
