import os

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from public_website.forms import InscritPoleEmploi


def index_view(request):
    return render(request, "public_website/index.html", {})


def accessibility_view(request):
    return render(request, "public_website/accessibility.html", {})


def login_view(request):
    return render(request, "public_website/login.html", {})


@login_required(login_url="/login/")
def pe_status_view(request):
    inscription_data = None
    form = InscritPoleEmploi
    APIPART_ENDPOINT = (
        "https://particulier-test.api.gouv.fr/api/v2/situations-pole-emploi"
    )

    if request.method == "POST":
        form = InscritPoleEmploi(request.POST)
        if form.is_valid():
            identifiantPE = form.cleaned_data["identifiantPE"]
            params = {"identifiant": identifiantPE}
            headers = {"X-Api-Key": os.getenv("API_PART_TOKEN")}
            response = requests.get(
                url=APIPART_ENDPOINT, headers=headers, params=params
            )
            inscription_data = response.json()

    context = {
        "form": form,
        "inscription_data": inscription_data,
    }
    return render(request, "public_website/pe_status.html", context)
