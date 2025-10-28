from django import forms
from . import models


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ['name', 'is_reproductive_female']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_reproductive_female': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # noqa
            # 'description': forms.Textarea(attrs{'class': 'form-control', 'rows': 3})  # noqa
        }
        labels = {
            'name': 'Nome',
            'is_reproductive_female': 'Fêmea reprodutiva',
        }
