from django.core.exceptions import ObjectDoesNotExist
from apps.account.application.ports.outbound.user_repo import UserRepository
from apps.account.domain.models import Account
from .models import AccountModel


class DjangoUserRepository(UserRepository):
    def find_by_id(self, user_id: int) -> Account | None:
        try:
            model = AccountModel.objects.get(id=user_id)
            return model.to_domain()
        except ObjectDoesNotExist:
            return None

    def find_by_email(self, email: str) -> Account | None:
        try:
            model = AccountModel.objects.get(email=email)
            return model.to_domain()
        except ObjectDoesNotExist:
            return None

    def exists_by_email(self, email: str) -> bool:
        return AccountModel.objects.filter(email=email).exists()

    def save(self, account: Account) -> int:
        if account.id is None:
            # Assumes account.password is a raw password
            if account.password is None:
                raise ValueError("Password is required for new user")
            model = AccountModel.objects.create_user(
                username=account.nickname,
                email=account.email,
                password=account.password,
            )
            return model.id
        else:
            try:
                model = AccountModel.objects.get(id=account.id)
                model.email = account.email
                model.username = account.nickname
                model.is_email_verified = account.is_email_verified

                # is_active in AbstractUser maps to status in domain
                if account.is_active:
                    model.is_active = True
                else:
                    model.is_active = False

                # Password changes are handled separately
                if account.password is not None:
                    model.set_password(account.password)

                model.save()
                return model.id
            except ObjectDoesNotExist:
                raise ValueError("User with given id does not exist")

    def check_password(self, user_id: int, raw_password: str) -> bool:
        try:
            model = AccountModel.objects.get(id=user_id)
            return model.check_password(raw_password)
        except ObjectDoesNotExist:
            return False

    def change_password(self, user_id: int, new_raw_password: str) -> None:
        try:
            model = AccountModel.objects.get(id=user_id)
            model.set_password(new_raw_password)
            model.save(update_fields=["password"])
        except ObjectDoesNotExist:
            # Should not happen in normal flow, but handle defensively
            raise ValueError("User with given id does not exist")

    def delete(self, user_id: int) -> None:
        try:
            model = AccountModel.objects.get(id=user_id)
            model.delete()
        except ObjectDoesNotExist:
            # User already deleted or doesn't exist
            pass
