from django.db import models
from django.core.exceptions import ValidationError
from inseminations.models import Insemination
from animals.models import Animal


# Tipo do nascimento / sexo do bezerro
BIRTH_TYPE_CHOICES = [
    ("F", "Fêmea"),
    ("M", "Macho"),
    ("SF", "Natimorto Fêmea"),
    ("SM", "Natimorto Macho"),
]


class Birth(models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.PROTECT,
        related_name='births'
    )
    insemination = models.ForeignKey(
        Insemination,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='births'
    )
    expected_birth = models.DateField(null=True, blank=True)
    expected_dry = models.DateField(null=True, blank=True)
    dry = models.DateField(null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    birth_type = models.CharField(
        max_length=2,
        choices=BIRTH_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Tipo do nascimento",
        help_text="Sexo/condição do bezerro no parto",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.animal.name)

    def clean(self):
        super().clean()
        if self.animal and not getattr(self.animal.category, 'is_reproductive_female', False):
            raise ValidationError("A categoria do animal selecionado não permite lançamento de parto.")
