from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class APICalls(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.PROTECT, related_name="calls")
    url = models.CharField(max_length=150, blank=False, null=False)
    PEid = models.CharField(max_length=150)
