from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class FarmListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # noqa
    model = models.Farm
    template_name = 'farm_list.html'
    context_object_name = 'farms'
    paginate_by = 10
    permission_required = 'farms.view_farm'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class FarmCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # noqa
    model = models.Farm
    template_name = "farm_create.html"
    form_class = forms.FarmForm
    success_url = reverse_lazy('farm_list')
    permission_required = 'farms.add_farm'


class FarmDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView): # noqa
    model = models.Farm
    template_name = 'farm_detail.html'
    permission_required = 'farms.view_farm'


class FarmUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # noqa
    model = models.Farm
    template_name = 'farm_update.html'
    form_class = forms.FarmForm
    success_url = reverse_lazy('farm_list')
    permission_required = 'farms.change_farm'


class FarmDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView): # noqa
    model = models.Farm
    template_name = 'farm_delete.html'
    success_url = reverse_lazy('farm_list')
    permission_required = 'farms.delete_farm'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                "Não é possível excluir esta propriedade porque existem registros vinculados (ex.: Animais)."
            )
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
