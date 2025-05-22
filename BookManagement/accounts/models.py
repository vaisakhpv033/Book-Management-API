from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for handling user creation."""

    def create_user(
        self,
        first_name,
        last_name,
        username,
        email,
        password=None,
        **extra_fields,
    ):
        """
        Create and return a regular user.

        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            username (str): Unique username.
            email (str): Unique email address.
            password (str, optional): User's password. Defaults to None.
            **extra_fields: Additional attributes.

        Raises:
            ValueError: If email or username is missing.

        Returns:
            User: The created user instance.
        """

        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(
        self, first_name, last_name, username, email, password=None, **extra_fields
    ):
        """
        Create and return a superuser with admin privileges.

        Args:
            first_name (str): Superuser's first name.
            last_name (str): Superuser's last name.
            username (str): Unique username.
            email (str): Unique email address.
            password (str, optional): Superuser's password. Defaults to None.
            **extra_fields: Additional attributes.

        Returns:
            User: The created superuser instance.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        return user


# validators
username_validator = RegexValidator(
    r"^[a-zA-Z0-9_]+$", "Usernames can only contain letters, numbers and underscores."
)

name_validator = RegexValidator(
    r"^[a-zA-Z\s]+$", "Enter a Valid name (Only alphabets and spaces)"
)


class User(AbstractBaseUser):
    """Custom User model that uses email as the unique identifier."""

    first_name = models.CharField(max_length=50, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])
    username = models.CharField(
        max_length=50, unique=True, validators=[username_validator]
    )
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
