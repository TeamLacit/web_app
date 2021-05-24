from django.db import models
from django.contrib.auth.models import AbstractUser
from account.models import UserManager


class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    project = models.ManyToManyField(Project)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.SmallIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT, null=True)
    post = models.CharField(max_length=200)
    block = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Task(models.Model):
    date = models.DateField()
    time_worked = models.PositiveBigIntegerField()
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    description = models.TextField()
