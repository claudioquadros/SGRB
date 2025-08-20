from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class InseminationListView(ListView):
    model = models.Insemination
    template_name = 'insemination_list.html'
    context_object_name = 'inseminations'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        queryset = queryset.order_by('expected_pregnancy')

        return queryset


class InseminationCreateView(CreateView):
    model = models.Insemination
    template_name = "Insemination_create.html"
    form_class = forms.InseminationRegisterForm
    success_url = reverse_lazy('insemination_list')


class InseminationDetailView(DetailView):
    model = models.Insemination
    template_name = 'insemination_detail.html'


class InseminationCheckView(UpdateView):
    model = models.Insemination
    template_name = 'insemination_check.html'
    form_class = forms.InseminationCheckForm
    success_url = reverse_lazy('insemination_list')
