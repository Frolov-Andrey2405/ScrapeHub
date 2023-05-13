from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    '''
    Custom user manager for the MyUser model.
    This manager provides the ability to create regular users and superusers.
    '''

    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    '''
    Custom user model representing a user of the job board website.
    The user is identified by their email address, and can be associated
    with a city and a programming language.
    They can also choose to receive email notifications about job postings.
    '''
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    city = models.ForeignKey(
        'app.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    language = models.ForeignKey(
        'app.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    send_email = models.BooleanField(default=False)

    objects = MyUserManager()

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
