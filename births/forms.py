from django import forms
from . import models
from django.utils.timezone import now


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
        widget=forms.DateInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'type': 'date'})  # noqa
    )

    class Meta:
        model = models.Birth
        fields = ['animal', 'date_of_insemination', 'expected_birth', 'expected_dry', 'dry', 'birth']  # noqa
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),  # noqa
            'expected_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # noqa
            'expected_dry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # noqa
            'dry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # noqa
            'birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # noqa
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

        # Preenche automaticamente o campo extra com a data da inseminação
        if self.instance and self.instance.insemination:
            self.fields['date_of_insemination'].initial = self.instance.insemination.date_of_insemination  # noqa

        # animal só para visualização
        self.fields['animal'].required = False


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
        # Preenche com a data atual se não tiver valor
        if not self.instance.dry:
            self.initial['dry'] = now().date()


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
        # Preencher automaticamente com a data de hoje
        if not self.instance.birth:
            self.initial['birth'] = now().date()
