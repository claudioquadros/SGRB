from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class BirthListView(ListView):
    model = models.Birth
    template_name = 'birth_list.html'
    context_object_name = 'births'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(animal__name__icontains=name)

        return queryset


class BirthCreateView(CreateView):
    model = models.Birth
    template_name = "birth_create.html"
    form_class = forms.BirthForm
    success_url = reverse_lazy('birth_list')


class BirthDetailView(DetailView):
    model = models.Birth
    template_name = 'birth_detail.html'


class BirthUpdateView(UpdateView):
    model = models.Birth
    template_name = 'birth_update.html'
    form_class = forms.BirthUpdateForm
    success_url = reverse_lazy('birth_list')


class BirthDeleteView(DeleteView):
    model = models.Birth
    template_name = 'birth_delete.html'
    success_url = reverse_lazy('birth_list')
