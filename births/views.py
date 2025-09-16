from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms


class BirthListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # noqa
    model = models.Birth
    template_name = 'birth_list.html'
    context_object_name = 'births'
    paginate_by = 10
    permission_required = 'births.view_birth'

    def get_queryset(self):
        queryset = super().get_queryset()

        farm_id = self.request.GET.get('farm')
        if farm_id:
            queryset = queryset.filter(animal__farm_id=farm_id)

        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(animal__name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from farms.models import Farm
        context["farms"] = Farm.objects.all()
        return context


class BirthCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # noqa
    model = models.Birth
    template_name = "birth_create.html"
    form_class = forms.BirthForm
    success_url = reverse_lazy('birth_list')
    permission_required = 'births.add_birth'


class BirthDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView): # noqa
    model = models.Birth
    template_name = 'birth_detail.html'
    permission_required = 'births.view_birth'


class BirthUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # noqa
    model = models.Birth
    template_name = 'birth_update.html'
    form_class = forms.BirthUpdateForm
    success_url = reverse_lazy('birth_list')
    permission_required = 'births.change_birth'


class CheckDryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # noqa
    model = models.Birth
    form_class = forms.BirthCheckDryUpdateForm
    template_name = 'birth_check_dry.html'
    permission_required = 'births.change_birth'

    def dispatch(self, request, *args, **kwargs):
        birth = self.get_object()

        if birth.dry or birth.birth:
            messages.error(request, "Não é possível lançar secagem para este animal.")  # noqa
            return redirect('birth_list')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Data de secagem registrada com sucesso!")  # noqa
        next_page = self.request.GET.get("next")
        if next_page == "overview":
            return str(reverse_lazy("animal_overview"))
        return str(reverse_lazy("birth_list"))

class CheckBirthUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # noqa
    model = models.Birth
    form_class = forms.BirthCheckBirthUpdateForm
    template_name = "birth_check_birth.html"
    permission_required = 'births.change_birth'

    def get_queryset(self):
        return models.Birth.objects.filter(birth__isnull=True)

    def get_success_url(self):
        next_page = self.request.GET.get("next")
        if next_page == "overview":
            return str(reverse_lazy("animal_overview"))
        return str(reverse_lazy("birth_list"))


class BirthDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView): # noqa
    model = models.Birth
    template_name = 'birth_delete.html'
    success_url = reverse_lazy('birth_list')
    permission_required = 'births.delete_birth'
