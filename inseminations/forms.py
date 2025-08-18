from django import forms
from .models import Insemination
from datetime import timedelta
from django.utils.timezone import now


class InseminationRegisterForm(forms.ModelForm):
    class Meta:
        model = Insemination
        fields = ['animal', 'date_of_insemination', 'expected_pregnancy']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'date_of_insemination': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date', 'style':
                    'max-width: 200px;'
                },
                format='%Y-%m-%d'
            ),
            'expected_pregnancy': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'style': 'max-width: 200px;'
                },
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'animal': 'Animal',
            'date_of_insemination': 'Data da Inseminação',
            'expected_pregnancy': 'Verificação da Prenhez',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define a data de hoje como padrão se não vier nada
        if not self.initial.get('date_of_insemination'):
            self.initial['date_of_insemination'] = now().date()

        date = self.initial.get('date_of_insemination')
        if date and not self.initial.get('expected_pregnancy'):
            self.initial['expected_pregnancy'] = date + timedelta(days=10)

    def clean(self):
        cleaned_data = super().clean()
        date_of_insemination = cleaned_data.get("date_of_insemination")

        if date_of_insemination:
            # Apenas sugere a data se o usuário não alterou
            if not cleaned_data.get("expected_pregnancy"):
                cleaned_data["expected_pregnancy"] = date_of_insemination + timedelta(days=10)  # noqa

        return cleaned_data
