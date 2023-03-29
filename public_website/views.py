from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from public_website.decorators import login_required_message
from public_website.forms import InscritPoleEmploiForm, StatutEtudiantBoursierForm
from public_website.models import APICall, Habilitation


def index_view(request):
    return render(request, "public_website/index.html", {})


@login_required_message()
def services_view(request):
    return render(request, "public_website/services.html", {})


def accessibility_view(request):
    return render(request, "public_website/accessibility.html", {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/services")
    return render(request, "public_website/login.html", {})


@login_required_message()
# @authorization_required_message(group_name="Artois Mobilités")
def pole_emploi_status_view(request):
    inscription_data = None
    form = InscritPoleEmploiForm
    authorized_group = Group.objects.get(name="Artois Mobilités")

    if (
        authorized_group not in request.user.groups.all()
        or not Habilitation.objects.filter(group=authorized_group).exists()
    ):
        error_message = "Vous êtes bien connecté·e, mais vous n'avez pas les droits pour accéder à cette page."
        messages.error(request, error_message)
        return redirect("/services/")

    if request.method == "POST":
        form = InscritPoleEmploiForm(request.POST)
        if form.is_valid():
            uri = "/situations-pole-emploi"

            api_call = APICall(
                user=request.user,
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
# @authorization_required_message(group_name="Brest Métropole")
def etudiant_boursier_status_view(request):
    inscription_data = None
    form = StatutEtudiantBoursierForm
    authorized_group = Group.objects.get(name="Brest Métropole")

    if (
        authorized_group not in request.user.groups.all()
        or not Habilitation.objects.filter(group=authorized_group).exists()
    ):
        error_message = "Vous êtes bien connecté·e, mais vous n'avez pas les droits pour accéder à cette page."
        messages.error(request, error_message)
        return redirect("/services/")

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
