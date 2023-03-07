from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from public_website.decorators import (
    authorization_required_message,
    login_required_message,
)
from public_website.forms import InscritPoleEmploiForm, StatutEtudiantBoursierForm
from public_website.models import APICall


def index_view(request):
    return render(request, "public_website/index.html", {})


# @login_required_message()
def services_view(request):
    return render(request, "public_website/services.html", {})


def accessibility_view(request):
    return render(request, "public_website/accessibility.html", {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/services")
    return render(request, "public_website/login.html", {})


# @login_required_message()
# @authorization_required_message(group_name="Artois Mobilités")
def pole_emploi_status_view(request):
    inscription_data = None
    form = InscritPoleEmploiForm

    if request.method == "POST":
        form = InscritPoleEmploiForm(request.POST)
        if form.is_valid():
            uri = "/situations-pole-emploi"

            anonymous_user = get_user_model().objects.get(username="anonymous_user")

            api_call = APICall(
                # user=request.user,
                user=anonymous_user,
                params='{"identifiant": "'
                + form.cleaned_data["identifiant_pole_emploi"]
                + '"}',
                uri=uri,
            )
            response = api_call.fetch()
            api_call.save()

            inscription_data = response.json()

    context = {
        "form": form,
        "inscription_data": inscription_data,
    }
    return render(request, "public_website/pole_emploi_status.html", context)


@login_required_message()
@authorization_required_message(group_name="Brest Métropole")
def etudiant_boursier_status_view(request):
    inscription_data = None
    form = StatutEtudiantBoursierForm

    if request.method == "POST":
        form = StatutEtudiantBoursierForm(request.POST)
        if form.is_valid():
            uri = "/etudiants-boursiers"

            api_call = APICall(
                user=request.user,
                params='{"ine": "' + form.cleaned_data["numero_ine"] + '"}',
                uri=uri,
            )
            response = api_call.fetch()
            api_call.save()

            inscription_data = response.json()

    context = {
        "form": form,
        "inscription_data": inscription_data,
    }
    return render(request, "public_website/etudiant_boursier_status.html", context)
