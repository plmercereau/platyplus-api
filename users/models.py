import binascii
import os

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class OwnedModel(models.Model):
    owned_by = models.ForeignKey('users.User', null=True, on_delete=models.deletion.DO_NOTHING)

    class Meta:
        abstract = True
