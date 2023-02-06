from django import forms


class InscritPoleEmploi(forms.Form):
    identifiantPE = forms.CharField(max_length=30, label='Identifiant Pôle Emploi', required=False)
