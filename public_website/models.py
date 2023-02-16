import os
from public_website.utils.hash import hash
import json

import requests
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class APICall(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.PROTECT, related_name="calls")
    uri = models.CharField(max_length=150, blank=False, null=False)
    params = models.CharField(max_length=150)

    @property
    def hash_params(self):
        hashed_params = hash(self.params)
        return hashed_params

    def fetch(self):
        url = os.environ["API_PARTICULIER_URL"] + self.uri
        response = requests.get(
            url=url,
            headers={"X-Api-Key": os.getenv("API_PART_TOKEN")},
            params=json.loads(self.params),
        )
        return response

    def save(self, *args, **kwargs):
          self.params = self.hash_params
          super(APICall, self).save(*args, **kwargs)
