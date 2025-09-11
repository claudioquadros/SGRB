from django import forms
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from . import models


class BirthForm(forms.ModelForm):

    class Meta:
        model = models.Birth
        fields = ['animal', 'birth', ]
        widgets = {
            'birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'style': 'max-width: 200px;',
                },
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'Animal': 'Animal',
            'birth': 'Nascimento',
        }


class BirthUpdateForm(forms.ModelForm):
    # Campo extra só para exibir a data da inseminação
    date_of_insemination = forms.DateField(
        label="Data da Inseminação",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': 'readonly'})  # noqa
    )

    class Meta:
        model = models.Birth
        fields = ['animal', 'date_of_insemination', 'expected_birth', 'expected_dry', 'dry', 'birth']  # noqa
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # noqa
            'expected_birth': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),  # noqa
            'expected_dry': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),  # noqa
            'dry': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),  # noqa
            'birth': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),  # noqa
        }
        labels = {
            'animal': 'Animal',
            'date_of_insemination': 'Data da Inseminação',
            'expected_birth': 'Data prevista para parto',
            'expected_dry': 'Data prevista para secagem',
            'dry': 'Data de secagem',
            'birth': 'Data do parto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.insemination:
            self.fields['date_of_insemination'].initial = (
                self.instance.insemination.date_of_insemination.strftime('%Y-%m-%d')  # noqa
            )
        self.fields['animal'].required = False

        for field in ['expected_birth', 'expected_dry', 'dry', 'birth']:
            value = getattr(self.instance, field)
            if value:
                # se for datetime, pega só a data
                if hasattr(value, 'date'):
                    value = value.date()
                self.fields[field].initial = value


class BirthCheckDryUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Birth
        fields = ['dry']
        widgets = {
            'dry': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }
        labels = {
            'dry': 'Data da Secagem',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.dry:
            self.initial['dry'] = now().date()

    def clean(self):
        cleaned_data = super().clean()
        dry = cleaned_data.get("dry")

        if not self.instance.expected_dry and dry:
            raise ValidationError("Este animal não possui previsão de secagem (novilha).")  # noqa

        return cleaned_data


class BirthCheckBirthUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Birth
        fields = ['birth']
        widgets = {
            'birth': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }
        labels = {
            'birth': 'Data do Parto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.birth:
            self.initial['birth'] = now().date()
