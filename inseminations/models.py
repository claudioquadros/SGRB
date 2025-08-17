from django.db import models
from animals.models import Animal


PRENHEZ_CHOICES = [
    ('S', 'Sim'),
    ('N', 'Não'),
]


class Insemination(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name='inseminations')  # noqa
    date_of_insemination = models.DateField()
    expected_pregnancy = models.DateField(null=True, blank=True)
    pregnancy_check = models.DateField(null=True, blank=True)
    is_pregnant = models.CharField(
        max_length=1,
        choices=PRENHEZ_CHOICES,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.animal.name)
