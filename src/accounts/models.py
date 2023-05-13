from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager

# Create your models here.


class MyUser(AbstractBaseUser):
    '''
    Custom user model
    '''
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    send_email = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
