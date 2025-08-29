from django.db import models
from categories.models import Category
from breeds.models import Breed
from farms.models import Farm


CULLING_REASON_CHOICES = [
    ("VD", "Venda"),
    ("MT", "Morte"),
]


class Animal(models.Model):
    name = models.CharField(max_length=100)
    birth = models.DateField(null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT, related_name='animais')  # noqa
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name='animais')  # noqa
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='animais') # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    culling_date = models.DateField(null=True, blank=True,verbose_name='Data da Baixa')  # noqa
    culling_reason = models.CharField(
        max_length=2,
        choices=CULLING_REASON_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
