from django import forms
from . import models


class CompanyForm(forms.ModelForm):

    class Meta:
        model = models.Company
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'description': forms.Textarea(attrs{'class': 'form-control', 'rows': 3})  # noqa
        }
        labels = {
            'name': 'Nome',
        }
