from django import forms
from . import models


class FarmForm(forms.ModelForm):

    class Meta:
        model = models.Farm
        fields = ['company', 'name']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'company': 'Companhia',
            'name': 'Nome da Propriedade',
        }
