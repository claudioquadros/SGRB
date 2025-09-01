from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class InseminationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # noqa
    model = models.Insemination
    template_name = 'insemination_list.html'
    context_object_name = 'inseminations'
    paginate_by = 10
    permission_required = 'inseminations.view_insemination'  # nome da app ação (view) nome do model  # noqa

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        queryset = queryset.order_by('expected_pregnancy')

        return queryset


class InseminationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # noqa
    model = models.Insemination
    template_name = "Insemination_create.html"
    form_class = forms.InseminationRegisterForm
    success_url = reverse_lazy('insemination_list')
    permission_required = 'inseminations.add_insemination'


class InseminationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):  # noqa
    model = models.Insemination
    template_name = 'insemination_detail.html'
    permission_required = 'inseminations.view_insemination'


class InseminationCheckView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):  # noqa
    model = models.Insemination
    template_name = 'insemination_check.html'
    form_class = forms.InseminationCheckForm
    success_url = reverse_lazy('insemination_list')
    permission_required = 'inseminations.change_insemination'


class InseminationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):  # noqa
    model = models.Insemination
    template_name = 'insemination_delete.html'
    success_url = reverse_lazy('insemination_list')
    permission_required = 'inseminations.delete_insemination'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_pregnant is not None:
            return redirect('insemination_list')
        return super().delete(request, *args, **kwargs)
