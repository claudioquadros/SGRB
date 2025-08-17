from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class CompanyListView(ListView):
    model = models.Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CompanyCreateView(CreateView):
    model = models.Company
    template_name = "company_create.html"
    form_class = forms.CompanyForm
    success_url = reverse_lazy('company_list')


class CompanyDetailView(DetailView):
    model = models.Company
    template_name = 'company_detail.html'


class CompanyUpdateView(UpdateView):
    model = models.Company
    template_name = 'company_update.html'
    form_class = forms.CompanyForm
    success_url = reverse_lazy('company_list')


class CompanyDeleteView(DeleteView):
    model = models.Company
    template_name = 'company_delete.html'
    success_url = reverse_lazy('company_list')
