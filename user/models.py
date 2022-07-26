import sys
from tabnanny import verbose
sys.dont_write_bytecode = True

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )

    username = models.CharField(
        verbose_name='名前',
        default='匿名',
        max_length=100,
    )

    is_active = models.BooleanField(
        verbose_name='状況',
        default=True)

    is_admin = models.BooleanField(default=False)

    date_joined = models.DateField(
        verbose_name="入会日",
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProperty(models.Model):
    OS = (('mac', 'Mac'),('windows', 'Windows'))
    user = models.OneToOneField(
        User,
        primary_key=True,
        unique=True,
        on_delete=models.CASCADE,
    )

    user_agent = models.CharField(
        verbose_name='ユーザーエージェント',
        max_length=1000,
    )

    os = models.CharField(
        verbose_name='OS',
        choices=OS,
        max_length=20,
    )