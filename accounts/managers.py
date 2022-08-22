from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password, email=None):
        if not phone_number:
            raise ValueError("this field is required")
        if not first_name:
            raise ValueError("this field is required")
        if not last_name:
            raise ValueError("this field is required")

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, phone_number, first_name, last_name, password, email=None
    ):
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
