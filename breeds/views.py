from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class BreedListView(ListView):
    model = models.Breed
    template_name = 'breed_list.html'
    context_object_name = 'breeds'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class BreedCreateView(CreateView):
    model = models.Breed
    template_name = "breed_create.html"
    form_class = forms.BreedForm
    success_url = reverse_lazy('breed_list')


class BreedDetailView(DetailView):
    model = models.Breed
    template_name = 'breed_detail.html'


class BreedUpdateView(UpdateView):
    model = models.Breed
    template_name = 'breed_update.html'
    form_class = forms.BreedForm
    success_url = reverse_lazy('breed_list')


class BreedDeleteView(DeleteView):
    model = models.Breed
    template_name = 'breed_delete.html'
    success_url = reverse_lazy('breed_list')
