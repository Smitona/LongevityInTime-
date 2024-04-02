from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


MIN_LENGTH_PASSWORD = 12
MAX_LENGTH_PASSWORD = 25


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('You must enter an email.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
        ],
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        help_text='Password must have an uppercase, lowercase, number '
                  'and special characters. 12-25 characters long.',
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
            MinLengthValidator(
                limit_value=MIN_LENGTH_PASSWORD,
                message='The password must be more than 12 characters long.'
            ),
            MaxLengthValidator(
                limit_value=MAX_LENGTH_PASSWORD,
                message='The password must be less than 25 characters long.'
            ),
        ],
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('email',)

    def __str__(self) -> str:
        return self.email
