class AccountError(Exception):
    """Base for account domain errors"""


class DuplicateEmailError(AccountError):
    def __init__(self, email: str):
        super().__init__(f"이미 가입된 이메일입니다: {email}")


class InvalidCredentials(AccountError):
    pass


class InvalidTokenError(AccountError):
    pass


class NotFoundError(AccountError):
    pass
