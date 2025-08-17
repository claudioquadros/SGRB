from django import forms
from . import models


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
