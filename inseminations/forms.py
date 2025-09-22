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
                    'type': 'date',
                    'style': 'max-width: 200px;'
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
        animal = cleaned_data.get("animal")

        # Impedir nova inseminação se já existir uma pendente para esse animal
        if animal:
            from .models import Insemination
            existe_pendente = Insemination.objects.filter(
                animal=animal,
                is_pregnant__isnull=True,   # ainda não verificado
                pregnancy_check__isnull=True
            ).exists()

            if existe_pendente:
                raise forms.ValidationError(
                    f"O animal {animal} já possui uma inseminação pendente de verificação."  # noqa
                )

        if date_of_insemination:
            if not cleaned_data.get("expected_pregnancy"):
                cleaned_data["expected_pregnancy"] = date_of_insemination + timedelta(days=10)  # noqa

        return cleaned_data


class InseminationCheckForm(forms.ModelForm):
    class Meta:
        model = Insemination
        fields = ['pregnancy_check', 'is_pregnant']
        widgets = {
            'pregnancy_check': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'style': 'max-width: 200px;',
                    'required': 'required'
                }
            ),
            'is_pregnant': forms.Select(
                attrs={
                    'class': 'form-select',
                    'style': 'max-width: 200px;',
                    'required': 'required'
                }
            )
        }
        labels = {
            'pregnancy_check': 'Data da Verificação da Prenhez',
            'is_pregnant': 'Está Prenha?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pregnancy_check:
            self.initial['pregnancy_check'] = self.instance.pregnancy_check.strftime('%Y-%m-%d')  # noqa
        else:
            self.initial['pregnancy_check'] = now().date().strftime('%Y-%m-%d')
