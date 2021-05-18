from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _


class Account(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class User(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    role = models.SmallIntegerField()
    # department = models.ForeignKey(Department, on_delete = models.RESTRICT)
    department = models.IntegerField()
    last_authorization = models.DateField()
    block = models.BooleanField(default=False)

