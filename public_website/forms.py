from django import forms


class InscritPoleEmploiForm(forms.Form):
    identifiant_pole_emploi = forms.CharField(
        max_length=30, label="Identifiant Pôle Emploi", required=True
    )


class StatutEtudiantBoursierForm(forms.Form):
    numero_ine = forms.CharField(max_length=30, label="Numéro INE", required=True)
