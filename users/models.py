from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
import uuid

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            password=password,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserAccount.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserAccount.DoesNotExist:
            return None


class UserAccount(AbstractBaseUser, PermissionsMixin):
    users_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    dateOfBirth = models.CharField(max_length=255)
    ssn = models.CharField(max_length=255)
    # plaid_access_token = models.CharField(max_length=255, blank=True, null=True)  # Add this line   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'address1', 'city',
                       'state', 'postalCode',
                       'dateOfBirth', 'ssn']

    def __str__(self):
        return self.email
    
    def check_password(self, raw_password):
        return super().check_password(raw_password)
    # def getFullName(self):
    #     return [self.first_name, self.last_name]
    
    # def getID(self):
    #     return self.id
    
    # def getEmail(self):
    #     return self.email

