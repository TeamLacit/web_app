from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    role = models.SmallIntegerField(default=1)
    # department = models.ForeignKey(Department, on_delete = models.RESTRICT)
    department = models.IntegerField(null=True)
    block = models.BooleanField(default=False)

    def __str__(self):
        return self.email
