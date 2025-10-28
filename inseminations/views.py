from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # noqa
from . import models, forms
from app.mixins import NextRedirectMixin


class InseminationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # noqa
    model = models.Insemination
    template_name = 'insemination_list.html'
    context_object_name = 'inseminations'
    paginate_by = 10
    permission_required = 'inseminations.view_insemination'  # nome da app ação (view) nome do model  # noqa

    def get_queryset(self):
        queryset = super().get_queryset()
        # Atualiza seleção de fazenda na sessão e aplica fallback
        if 'farm' in self.request.GET:
            self.request.session['selected_farm_id'] = self.request.GET.get('farm') or None  # noqa
        farm_id = self.request.GET.get('farm') or self.request.session.get('selected_farm_id')  # noqa
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

class InseminationCreateView(LoginRequiredMixin, PermissionRequiredMixin, NextRedirectMixin, CreateView):  # noqa
    model = models.Insemination
    template_name = "insemination_create.html"
    form_class = forms.InseminationRegisterForm
    success_url = 'insemination_list'
    permission_required = 'inseminations.add_insemination'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra apenas fêmeas reprodutivas e, se houver, pela fazenda
        from animals.models import Animal
        farm_id = self.request.GET.get("farm") or self.request.session.get('selected_farm_id')  # noqa
        if 'animal' in form.fields:
            try:
                base_qs = Animal.objects.filter(category__is_reproductive_female=True)
                if farm_id:
                    base_qs = base_qs.filter(farm_id=int(farm_id))
                form.fields['animal'].queryset = base_qs
            except (ValueError, TypeError):
                form.fields['animal'].queryset = Animal.objects.filter(category__is_reproductive_female=True)

        animal_id = self.request.GET.get("animal")
        if animal_id and 'animal' in form.fields:
            try:
                # garante que seja int (pk)
                form.fields['animal'].initial = int(animal_id)
            except (ValueError, TypeError):
                pass
        return form

    def get_success_url(self):
        next_page = self.request.GET.get("next")
        if next_page == "overview":
            return str(reverse("animal_overview"))
        return str(reverse("insemination_list"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Expor configuração para uso no template (JS)
        from app.config import get_int
        context["PREGNANCY_CHECK_OFFSET_DAYS"] = get_int('PREGNANCY_CHECK_OFFSET_DAYS', 10)  # noqa
        return context

class InseminationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):  # noqa
    model = models.Insemination
    template_name = 'insemination_detail.html'
    permission_required = 'inseminations.view_insemination'

class InseminationCheckView(LoginRequiredMixin, PermissionRequiredMixin, NextRedirectMixin, UpdateView):  # noqa
    model = models.Insemination
    template_name = 'insemination_check.html'
    form_class = forms.InseminationCheckForm
    success_url = 'insemination_list'
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
