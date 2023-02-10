import os

import requests
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class APICall(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.PROTECT, related_name="calls")
    url = models.CharField(max_length=150, blank=False, null=False)
    queried_id = models.CharField(max_length=150)

    def fetch(self):
        APIPART_ENDPOINT = (
            "https://particulier-test.api.gouv.fr/api/v2/situations-pole-emploi"
        )
        response = requests.get(
            url=APIPART_ENDPOINT,
            headers={"X-Api-Key": os.getenv("API_PART_TOKEN")},
            params={"identifiant": self.queried_id},
        )
        return response
