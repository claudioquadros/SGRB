from django.views.generic import ListView
from django.db.models import Subquery, OuterRef
from django.utils.timezone import now
from datetime import timedelta
from animals.models import Animal
from inseminations.models import Insemination
from births.models import Birth
from farms.models import Farm


class AnimalOverviewListView(ListView):
    model = Animal
    template_name = "animal_overview.html"
    context_object_name = "animals"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        last_insemination = Insemination.objects.filter(
            animal=OuterRef('pk')
        ).order_by('-date_of_insemination')

        last_birth = Birth.objects.filter(
            insemination__animal=OuterRef('pk'),
            insemination=Subquery(last_insemination.values('id')[:1])
        ).order_by('-created_at')

        farm_id = self.request.GET.get('farm')
        if farm_id:
            queryset = queryset.filter(farm_id=farm_id)

        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        queryset = queryset.annotate(
            ultima_inseminacao_id=Subquery(last_insemination.values('id')[:1]),
            ultima_inseminacao=Subquery(last_insemination.values('date_of_insemination')[:1]),  # noqa
            prenhez_verificacao=Subquery(last_insemination.values('expected_pregnancy')[:1]),  # noqa
            prenhez_verificada=Subquery(last_insemination.values('pregnancy_check')[:1]),  # noqa
            esta_prenha=Subquery(last_insemination.values('is_pregnant')[:1]),
            parto_previsto=Subquery(last_birth.values('expected_birth')[:1]),
            secagem_prevista=Subquery(last_birth.values('expected_dry')[:1]),
            secagem=Subquery(last_birth.values('dry')[:1]),
            parto=Subquery(last_birth.values('birth')[:1]),
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["farms"] = Farm.objects.all()
        context["today"] = now().date()
        context["today_plus_10"] = now().date() + timedelta(days=10)
        return context
