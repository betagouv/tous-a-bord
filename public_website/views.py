from django.contrib import messages
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import redirect, render

from public_website.decorators import (
    authorization_required_message,
    login_required_message,
)
from public_website.forms import (
    DemoExportForm,
    DemoNotificationForm,
    InscritPoleEmploiForm,
    StatutEtudiantBoursierForm,
)
from public_website.models import APICall, Habilitation, Import, Item
from public_website.utils import email_provider, sms_provider
from public_website.utils.grist import build_dataset


def index_view(request):
    return render(request, "public_website/index.html", {})


@login_required_message()
def services_view(request):
    return render(request, "public_website/services.html", {})


@login_required_message()
def demo_view(request):
    return render(request, "public_website/demo/index.html", {})


@login_required_message()
def demo_export_select_view(request):
    if request.method == "POST":
        form = DemoExportForm(request.POST)
        if not form.is_valid():
            messages.warning(request, message="La commune n'a pas été renseignée.")
        else:
            with transaction.atomic():
                import_instance = Import(user=request.user)
                import_instance.save()
                for item_data in build_dataset(form.cleaned_data["commune"]):
                    i = Item(import_instance=import_instance, value=item_data)
                    i.save()
                return redirect(f"/demo/import/{import_instance.id}")

    return render(
        request, "public_website/demo/export/select.html", {"form": DemoExportForm}
    )


@login_required_message()
def demo_import_index_view(request):
    return render(request, "public_website/demo/index.html", {})


@login_required_message()
def demo_import_item_view(request, id):
    if request.method == "POST":
        form = DemoNotificationForm(request.POST)
        if not form.is_valid():
            messages.warning(request, message="BUG!")
        elif form.cleaned_data["item"].import_instance.user != request.user:
            messages.warning(request, message="Hacking?!?")
        else:
            data = form.cleaned_data["item"].value["fields"]
            if form.cleaned_data["channel"] == "sms":
                sms_provider.send_notification_sms(data["TEL"])
                messages.success(request, message=f"SMS envoyé au {data['TEL']} !")
            else:
                name = f"{data['PRENOM']} {data['NOM']}"
                email = data["EMAIL"]
                email_provider.send_notification_email(email, name)
                messages.success(request, message=f"EMAIL envoyé à {name} <{email}> !")

    import_instance = request.user.imports.get(pk=id)
    return render(
        request,
        "public_website/demo/import/item.html",
        {
            "import": import_instance,
            "items": import_instance.items.all(),
            "data_headers": [
                "PRENOM",
                "NOM",
                "TEL",
                "EMAIL",
                "COMMUNE",
                "MATRICULE",
                "QF",
                "RSA",
            ],
        },
    )


def accessibility_view(request):
    return render(request, "public_website/accessibility.html", {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/services")
    return render(request, "public_website/login.html", {})


@login_required_message()
@authorization_required_message(group_name="Artois Mobilités")
def pole_emploi_status_view(request):
    inscription_data = None
    form = InscritPoleEmploiForm
    authorized_group = Group.objects.get(name="Artois Mobilités")

    if not Habilitation.objects.filter(group=authorized_group).exists():
        messages.warning(
            request,
            message="Pas d'habilitation trouvée pour votre groupe. Contactez-nous à tousabord@beta.gouv.fr.",
        )

    if request.method == "POST":
        form = InscritPoleEmploiForm(request.POST)
        if form.is_valid():
            uri = "/api/v2/situations-pole-emploi"

            api_call = APICall(
                user=request.user,
                habilitation=Habilitation.objects.get(group=authorized_group),
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
    authorized_group = Group.objects.get(name="Brest Métropole")

    if not Habilitation.objects.filter(group=authorized_group).exists():
        messages.warning(
            request,
            message="Pas d'habilitation trouvée pour votre groupe. Contactez-nous à tousabord@beta.gouv.fr.",
        )

    if request.method == "POST":
        form = StatutEtudiantBoursierForm(request.POST)
        if form.is_valid():
            uri = "/api/v2/etudiants-boursiers"

            api_call = APICall(
                user=request.user,
                habilitation=Habilitation.objects.get(group=authorized_group),
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


def demo_imports_index_view(request):
    return render(
        request,
        "public_website/demo/imports.html",
        context={"imports": request.user.imports.all()},
    )


def legal_notice_view(request):
    return render(request, "public_website/mentions-legales.html", context={})
