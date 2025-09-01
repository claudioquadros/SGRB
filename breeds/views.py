from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class BreedListView(LoginRequiredMixin, PermissionRequiredMixin, ListView): # noqa
    model = models.Breed
    template_name = 'breed_list.html'
    context_object_name = 'breeds'
    paginate_by = 10
    permission_required = 'breeds.view_breed'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class BreedCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView): # noqa
    model = models.Breed
    template_name = "breed_create.html"
    form_class = forms.BreedForm
    success_url = reverse_lazy('breed_list')
    permission_required = 'breeds.add_breed'


class BreedDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView): # noqa
    model = models.Breed
    template_name = 'breed_detail.html'
    permission_required = 'breeds.view_breed'


class BreedUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # noqa
    model = models.Breed
    template_name = 'breed_update.html'
    form_class = forms.BreedForm
    success_url = reverse_lazy('breed_list')
    permission_required = 'breeds.change_breed'


class BreedDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView): # noqa
    model = models.Breed
    template_name = 'breed_delete.html'
    success_url = reverse_lazy('breed_list')
    permission_required = 'breeds.delete_breed'
