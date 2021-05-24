from django.db import models
from user.models import Department


class UnregisteredUser(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    post = models.CharField(max_length=200)
    role = models.SmallIntegerField(default=3)