from django.db import models
from authorization.models import User


class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    department = models.ManyToManyField(Department)

    def __str__(self):
        return self.name


class Task(models.Model):
    date = models.DateField()
    time_worked = models.TimeField()
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    description = models.TextField()
