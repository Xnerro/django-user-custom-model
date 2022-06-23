from django.db.models import EmailField, CharField, BooleanField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Username Already use")
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_staff = True
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = CharField("username", max_length=250, unique=True)
    email = EmailField("email address", max_length=250)
    password = CharField("password", max_length=100)
    is_active = BooleanField("active", default=True)
    is_staff = BooleanField("staff", default=False)
    is_admin = BooleanField("admin", default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
