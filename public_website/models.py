import json
import os

import requests
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from public_website.utils.hash import hash


class Habilitation(models.Model):
    token = models.CharField(max_length=150, blank=False, null=False)
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT, related_name="habilitation"
    )

    def __str__(self):
        return f"Token {self.group}"


class User(AbstractUser):
    def groups_list(self):
        return ", ".join([group.name for group in self.groups.all()])


class APICall(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.PROTECT, related_name="calls")
    uri = models.CharField(max_length=150, blank=False, null=False)
    params = models.CharField(max_length=150)
    habilitation = models.ForeignKey(Habilitation, models.PROTECT, related_name="uses")

    @property
    def hash_params(self):
        hashed_params = hash(self.params)
        return hashed_params

    def fetch(self):
        url = os.environ["API_PARTICULIER_URL"] + self.uri
        response = requests.get(
            url=url,
            headers={"X-Api-Key": self.habilitation.token},
            params=json.loads(self.params),
        )
        return response

    def save(self, *args, **kwargs):
        self.params = self.hash_params
        super(APICall, self).save(*args, **kwargs)


class BrestWebhookMessage(models.Model):
    received_at = models.DateTimeField(help_text="When we received the event.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]
