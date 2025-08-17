from django.db import models
from inseminations.models import Insemination
from animals.models import Animal


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.animal.name)
