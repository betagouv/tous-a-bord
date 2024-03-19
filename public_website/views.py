import zipfile
from tempfile import NamedTemporaryFile

import pandas as pd
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
from public_website.models import APICall, Export, Habilitation, Import, Item
from public_website.utils import email_provider, hubee, sms_provider
from public_website.utils.grist import build_csv


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
            data = build_csv(form.cleaned_data["commune"])
            with NamedTemporaryFile("w") as csv:
                csv.write(data)
                csv.flush()

                with NamedTemporaryFile(
                    prefix="archive_", suffix=".zip"
                ) as archive_fid:
                    with zipfile.ZipFile(archive_fid, "w") as archive:
                        archive.write(csv.name, "data.csv")
                    archive_fid.flush()

                    hubee_token = hubee.get_token("OSL")
                    company_register, branch_code = "24670048800017", "67482"
                    hubee.send(
                        company_register, branch_code, archive_fid.name, hubee_token
                    )
                    export_instance = Export(user=request.user)
                    export_instance.save()
            messages.success(request, message="Données envoyées via HubEE")
            return redirect("/demo")

    return render(
        request, "public_website/demo/export/select.html", {"form": DemoExportForm}
    )


@login_required_message()
def demo_import_index_view(request):
    if request.method == "POST":

        hubee_token = hubee.get_token("SI")
        company_register = "18000000000000"
        notifications = hubee.get_notifications(hubee_token)
        interesting_notifications = [
            n
            for n in notifications
            if n["transmitter"]["companyRegister"] == company_register
        ]

        for n in interesting_notifications:
            case = hubee.get_case(n["caseId"], hubee_token)
            if case["externalId"] != "DEMO_TAB_case":
                continue
            for attachment in case["attachments"]:
                with NamedTemporaryFile(
                    prefix="archive_", suffix=".zip"
                ) as archive_fid:
                    attachment_data = hubee.get_attachment(
                        case["id"], attachment["id"], hubee_token
                    )
                    archive_fid.write(attachment_data.content)
                    archive_fid.flush()

                    with zipfile.ZipFile(archive_fid, "r") as archive:
                        for file in archive.infolist():
                            with archive.open(file.filename) as data:
                                df = pd.read_csv(data, dtype="str")
                                with transaction.atomic():
                                    import_instance = Import(user=request.user)
                                    import_instance.save()
                                    import json

                                    for i in df.index:
                                        item = Item(
                                            import_instance=import_instance,
                                            value=json.loads(df.loc[i].to_json()),
                                        )
                                        item.save()

                                    messages.success(
                                        request,
                                        message="Données récupérées depuis HubEE",
                                    )

                                    hubee.patch_case(
                                        n["caseId"], {"status": "DONE"}, hubee_token
                                    )
                                    hubee.delete_notification(n["id"], hubee_token)

                                    return redirect(
                                        f"/demo/import/{import_instance.id}"
                                    )

        messages.warning(request, message="Pas de donnée à récupérer depuis HubEE")
    return render(request, "public_website/demo/import/index.html", {})


@login_required_message()
def demo_import_item_view(request, id):
    if request.method == "POST":
        form = DemoNotificationForm(request.POST)
        if not form.is_valid():
            messages.warning(request, message="BUG!")
        elif form.cleaned_data["item"].import_instance.user != request.user:
            messages.warning(request, message="Hacking?!?")
        else:
            data = form.cleaned_data["item"].value
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
                "ID",
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
