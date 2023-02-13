from django import forms


class InscritPoleEmploi(forms.Form):
    identifiant_pole_emploi = forms.CharField(max_length=30, label='Identifiant Pôle Emploi', required=False)
