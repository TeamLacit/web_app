from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _
from user.models import Department

class User(AbstractUser):
    role = models.SmallIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    post = models.CharField(max_length=200)
    block = models.BooleanField(default=False)

    def __str__(self):
        return self.email
