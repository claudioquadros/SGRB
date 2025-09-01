from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class CompanyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # noqa
    model = models.Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    paginate_by = 10
    permission_required = 'companies.view_company'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # noqa
    model = models.Company
    template_name = "company_create.html"
    form_class = forms.CompanyForm
    success_url = reverse_lazy('company_list')
    permission_required = 'companies.add_company'


class CompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):  # noqa
    model = models.Company
    template_name = 'company_detail.html'
    permission_required = 'companies.view_company'


class CompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):  # noqa
    model = models.Company
    template_name = 'company_update.html'
    form_class = forms.CompanyForm
    success_url = reverse_lazy('company_list')
    permission_required = 'companies.change_company'


class CompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):  # noqa
    model = models.Company
    template_name = 'company_delete.html'
    success_url = reverse_lazy('company_list')
    permission_required = 'companies.delete_company'
