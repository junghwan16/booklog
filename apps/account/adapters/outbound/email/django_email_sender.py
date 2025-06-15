from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from apps.account.application.ports.outbound.email_sender import EmailSenderPort


class DjangoEmailSender(EmailSenderPort):
    def send_email_verify(self, to_email: str, token: str) -> None:
        send_mail(
            subject="이메일 인증 링크",
            message=f"이메일 인증 링크: http://localhost:8000/account/email/verify/{token}",
            from_email="noreply@example.com",
            recipient_list=[to_email],
        )

    def send_password_reset(self, to_email: str, uid: str, token: str) -> None:
        uidb64 = urlsafe_base64_encode(force_bytes(uid))
        send_mail(
            subject="비밀번호 재설정 링크",
            message=f"비밀번호 재설정 링크: http://localhost:8000/account/password/reset/{uidb64}/{token}",
            from_email="noreply@example.com",
            recipient_list=[to_email],
        )
