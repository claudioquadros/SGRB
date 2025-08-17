from django import forms
from .models import Insemination


class InseminationRegisterForm(forms.ModelForm):
    class Meta:
        model = Insemination
        fields = ['animal', 'date_of_insemination', 'expected_pregnancy']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'date_of_insemination': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'expected_pregnancy': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'animal': 'Animal',
            'date_of_insemination': 'Data da Inseminação',
            'expected_pregnancy': 'Verificação da Prenhez',
        }
