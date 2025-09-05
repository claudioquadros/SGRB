from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class AnimalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Animal
    template_name = 'animal_list.html'
    context_object_name = 'animals'
    paginate_by = 10
    permission_required = 'animals.view_animal'

    def get_queryset(self):
        queryset = super().get_queryset()

        farm_id = self.request.GET.get('farm')
        if farm_id:
            queryset = queryset.filter(farm_id=farm_id)

        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from farms.models import Farm
        context["farms"] = Farm.objects.all()
        return context

class AnimalCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # noqa
    model = models.Animal
    template_name = "animal_create.html"
    form_class = forms.AnimalForm
    success_url = reverse_lazy('animal_list')
    permission_required = 'animals.add_animal'


class AnimalDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):  # noqa
    model = models.Animal
    template_name = 'animal_detail.html'
    permission_required = 'animals.view_animal'


class AnimalUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):  # noqa
    model = models.Animal
    template_name = 'animal_update.html'
    form_class = forms.AnimalForm
    success_url = reverse_lazy('animal_list')
    permission_required = 'animals.change_animal'


class AnimalCullingView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # noqa
    model = models.Animal
    template_name = 'animal_culling.html'
    form_class = forms.AnimalCullingForm
    success_url = reverse_lazy('animal_list')
    permission_required = 'animals.change_animal'


class AnimalDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView): # noqa
    model = models.Animal
    template_name = 'animal_delete.html'
    success_url = reverse_lazy('animal_list')
    permission_required = 'animals.delete_animal'
