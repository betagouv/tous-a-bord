from django import forms

from public_website.models import Item
from public_website.utils.grist import get_communes


class InscritPoleEmploiForm(forms.Form):
    identifiant_pole_emploi = forms.CharField(
        max_length=30, label="Identifiant Pôle Emploi", required=True
    )


class StatutEtudiantBoursierForm(forms.Form):
    numero_ine = forms.CharField(max_length=30, label="Numéro INE", required=True)


def get_values():
    data = get_communes()

    def get_label(record):
        f = record["fields"]
        return f"{f['COMMUNE']} ({f['Nb_familles']} familles / {f['Nb_personnes']} personnes)"

    return [(c["fields"]["COMMUNE"], get_label(c)) for c in data["records"]]


class DemoExportForm(forms.Form):
    commune = forms.ChoiceField(choices=(), label="Commune à exporter", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["commune"].choices = get_values()


class DemoNotificationForm(forms.Form):
    channel = forms.ChoiceField(
        choices=[("sms", "sms"), ("email", "email")], required=True
    )
    item = forms.ModelChoiceField(queryset=Item.objects)
