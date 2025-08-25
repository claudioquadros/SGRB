from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .models import Insemination
from births.models import Birth


@receiver(post_save, sender=Insemination)
def create_birth_for_pregnant_update(sender, instance, **kwargs):
    print("Passou por aqui")
    if instance.is_pregnant == "Sim":
        # Evita duplicar se já existe parto para esta inseminação
        if not Birth.objects.filter(insemination=instance).exists():
            print('também passou por aqui')
            expected_birth = instance.date_of_insemination + timedelta(days=282)  # noqa
            expected_dry = expected_birth - timedelta(days=50)

            Birth.objects.create(
                animal=instance.animal,
                insemination=instance,
                expected_birth=expected_birth,
                expected_dry=expected_dry,
            )
