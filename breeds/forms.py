from django import forms
from . import models


class BreedForm(forms.ModelForm):

    class Meta:
        model = models.Breed
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'description': forms.Textarea(attrs{'class': 'form-control', 'rows': 3})  # noqa
        }
        labels = {
            'name': 'Nome',
        }
