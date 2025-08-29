from django import forms
from . import models
from django.utils.timezone import now


class AnimalForm(forms.ModelForm):

    class Meta:
        model = models.Animal
        fields = ['farm', 'name', 'breed', 'category', 'birth',]
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
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
            'farm': 'Propriedade',
            'name': 'Nome',
            'breed': 'Raça',
            'category': 'Categoria',
            'birth': 'Nascimento',
        }


class AnimalCullingForm(forms.ModelForm):

    class Meta:
        model = models.Animal
        fields = ['culling_date', 'culling_reason',]
        widgets = {
            'culling_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'style': 'max-width: 200px;',
                },
                format='%Y-%m-%d'
            ),
            'culling_reason': forms.Select(
                    attrs={
                        'class': 'form-select',
                        'style': 'max-width: 200px;'
                    }
            ),
        }
        labels = {
            'culling_date': 'Data da Baixa',
            'culling_reason': 'Motivo da Baixa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.culling_date:
            self.initial['culling_date'] = now().date()
