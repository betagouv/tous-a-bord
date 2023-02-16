from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from public_website.decorators import belongs_to_group

from public_website.forms import InscritPoleEmploiForm, StatutEtudiantBoursierForm
from public_website.models import APICall


def index_view(request):
    return render(request, "public_website/index.html", {})


def accessibility_view(request):
    return render(request, "public_website/accessibility.html", {})


def login_view(request):
    return render(request, "public_website/login.html", {})

@user_passes_test(belongs_to_group("Artois Mobilités"))
def pole_emploi_status_view(request):
    inscription_data = None
    form = InscritPoleEmploiForm

    if request.method == "POST":
        form = InscritPoleEmploiForm(request.POST)
        if form.is_valid():
            uri = "/situations-pole-emploi"
            
            api_call = APICall(
                user=request.user,
                queried_id=form.cleaned_data["identifiant_pole_emploi"],
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

@user_passes_test(belongs_to_group("Brest Métropole"))
def etudiant_boursier_status_view(request):
    inscription_data = None
    form = StatutEtudiantBoursierForm

    if request.method == "POST":
        form = StatutEtudiantBoursierForm(request.POST)
        if form.is_valid():
            uri = "/etudiants-boursiers"
            
            api_call = APICall(
                user=request.user,
                queried_id=form.cleaned_data["numero_ine"],
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
