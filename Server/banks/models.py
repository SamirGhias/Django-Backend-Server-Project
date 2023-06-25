from django.db import models
from django.contrib.auth.models import User
from django.db.models import SET_NULL, CASCADE


# Create your models here.


class Bank(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    inst_num = models.CharField(max_length=100, null=False)
    swift_code = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(to=User, null=True, on_delete=SET_NULL)

    # id = id()
    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, null=False)
    transit_num = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    capacity = models.PositiveIntegerField(null=True)
    last_modified = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, null=False, on_delete=CASCADE)

    def __str__(self):
        return self.name
