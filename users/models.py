from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)

class UserAccountManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **kwargs):
        print("Creating user with:", username, email, kwargs)  # Debug print
        if not username:
            raise ValueError('The Username field is required')

        if not email:
            raise ValueError('The Email field is required')

        # Normalize email and create user model
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **kwargs)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipCode = models.CharField(max_length=15)

    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, max_length=255)

    username = models.CharField(max_length=50, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 
                       'address', 'city',
                       'state', 'zipCode',
                       'phone',
                       'username',
                       'password']

    def __str__(self):
        return self.email
