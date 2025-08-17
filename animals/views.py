from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class AnimalListView(ListView):
    model = models.Animal
    template_name = 'animal_list.html'
    context_object_name = 'animals'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class AnimalCreateView(CreateView):
    model = models.Animal
    template_name = "animal_create.html"
    form_class = forms.AnimalForm
    success_url = reverse_lazy('animal_list')


class AnimalDetailView(DetailView):
    model = models.Animal
    template_name = 'animal_detail.html'


class AnimalUpdateView(UpdateView):
    model = models.Animal
    template_name = 'animal_update.html'
    form_class = forms.AnimalForm
    success_url = reverse_lazy('animal_list')


class AnimalDeleteView(DeleteView):
    model = models.Animal
    template_name = 'animal_delete.html'
    success_url = reverse_lazy('animal_list')
