from __future__ import annotations
from typing import List, Tuple

from apps.account.application.ports.outbound.email_sender import EmailSenderPort


class FakeEmailSender(EmailSenderPort):
    def __init__(self):
        self.sent_emails: List[Tuple[str, str]] = []
        self.sent_password_resets: List[Tuple[str, str, str]] = []

    def send_email_verify(self, to_email: str, token: str) -> None:
        self.sent_emails.append((to_email, token))

    def send_password_reset(self, to_email: str, uid: str, token: str) -> None:
        self.sent_password_resets.append((to_email, uid, token))
