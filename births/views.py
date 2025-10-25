from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from django.utils.timezone import now
from datetime import timedelta
from app.config import get_int
from . import models, forms
from app.mixins import NextRedirectMixin


class BirthListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # noqa
    model = models.Birth
    template_name = 'birth_list.html'
    context_object_name = 'births'
    paginate_by = 10
    permission_required = 'births.view_birth'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Atualiza seleção de fazenda na sessão e aplica fallback
        if 'farm' in self.request.GET:
            self.request.session['selected_farm_id'] = self.request.GET.get('farm') or None
        farm_id = self.request.GET.get('farm') or self.request.session.get('selected_farm_id')
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
        # Para destacar ações conforme janela do overview
        context["today"] = now().date()
        context["today_plus_10"] = now().date() + timedelta(days=get_int('UPCOMING_WINDOW_DAYS', 10))
        return context


class BirthCreateView(LoginRequiredMixin, PermissionRequiredMixin, NextRedirectMixin, CreateView):  # noqa
    model = models.Birth
    template_name = "birth_create.html"
    form_class = forms.BirthForm
    success_url = 'birth_list'
    permission_required = 'births.add_birth'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Prefill e filtro de Animal pela fazenda selecionada no filtro
        from animals.models import Animal
        farm_id = self.request.GET.get("farm") or self.request.session.get('selected_farm_id')
        if farm_id and 'animal' in form.fields:
            try:
                form.fields['animal'].queryset = Animal.objects.filter(farm_id=int(farm_id))
            except (ValueError, TypeError):
                # Se inválido, mantém queryset padrão
                pass

        animal_id = self.request.GET.get("animal")
        if animal_id and 'animal' in form.fields:
            try:
                form.fields['animal'].initial = int(animal_id)
            except (ValueError, TypeError):
                pass
        return form


class BirthDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView): # noqa
    model = models.Birth
    template_name = 'birth_detail.html'
    permission_required = 'births.view_birth'


class BirthUpdateView(LoginRequiredMixin, PermissionRequiredMixin, NextRedirectMixin, UpdateView): # noqa
    model = models.Birth
    template_name = 'birth_update.html'
    form_class = forms.BirthUpdateForm
    success_url = 'birth_list'
    permission_required = 'births.change_birth'


class CheckDryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, NextRedirectMixin, UpdateView): # noqa
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

    # def get_success_url(self):
    #     messages.success(self.request, "Data de secagem registrada com sucesso!")  # noqa
    #     next_page = self.request.GET.get("next")
    #     if next_page == "overview":
    #         return str(reverse_lazy("animal_overview"))
    #     return str(reverse_lazy("birth_list"))

class CheckBirthUpdateView(LoginRequiredMixin, PermissionRequiredMixin, NextRedirectMixin, UpdateView): # noqa
    model = models.Birth
    form_class = forms.BirthCheckBirthUpdateForm
    template_name = "birth_check_birth.html"
    permission_required = 'births.change_birth'

    def get_queryset(self):
        return models.Birth.objects.filter(birth__isnull=True)

    # def get_success_url(self):
    #     next_page = self.request.GET.get("next")
    #     if next_page == "overview":
    #         return str(reverse_lazy("animal_overview"))
    #     return str(reverse_lazy("birth_list"))


class BirthDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView): # noqa
    model = models.Birth
    template_name = 'birth_delete.html'
    success_url = reverse_lazy('birth_list')
    permission_required = 'births.delete_birth'
