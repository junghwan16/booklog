from abc import ABC, abstractmethod


class EmailSenderPort(ABC):
    @abstractmethod
    def send_email_verify(self, to_email: str, token: str) -> None: ...
    @abstractmethod
    def send_password_reset(self, to_email: str, token: str) -> None: ...
