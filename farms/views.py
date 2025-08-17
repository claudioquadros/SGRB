from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class FarmListView(ListView):
    model = models.Farm
    template_name = 'farm_list.html'
    context_object_name = 'farms'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class FarmCreateView(CreateView):
    model = models.Farm
    template_name = "farm_create.html"
    form_class = forms.FarmForm
    success_url = reverse_lazy('farm_list')


class FarmDetailView(DetailView):
    model = models.Farm
    template_name = 'farm_detail.html'


class FarmUpdateView(UpdateView):
    model = models.Farm
    template_name = 'farm_update.html'
    form_class = forms.FarmForm
    success_url = reverse_lazy('farm_list')


class FarmDeleteView(DeleteView):
    model = models.Farm
    template_name = 'farm_delete.html'
    success_url = reverse_lazy('farm_list')
