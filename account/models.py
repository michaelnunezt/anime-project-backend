from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):

    def create_user(self, username: str, email: str, password: str = None, **extra_fields: dict):
        """
        Creates and saves a new user with the given email and password.

        :param username: unique username of the user
        :param email: unique email of the user
        :param password: password of the user, to be hashed and saved
        :param extra_fields: other fields
        :return: New created user object
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given username, email, and password.

        :param username: unique username of the user
        :param email: unique email of the user
        :param password: password of the user, to be hashed and saved
        :param extra_fields: other fields
        :return: New created user object
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    user model that uses email instead of username for authentication.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)  # isAdmin field equivalent
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(blank=True, null=True)
    my_list = models.ManyToManyField('self', blank=True, symmetrical=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
