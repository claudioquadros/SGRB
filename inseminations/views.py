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

class InseminationCreateView(LoginRequiredMixin, PermissionRequiredMixin, NextRedirectMixin, CreateView):  # noqa
    model = models.Insemination
    template_name = "Insemination_create.html"
    form_class = forms.InseminationRegisterForm
    success_url = 'insemination_list'
    permission_required = 'inseminations.add_insemination'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
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

    def get_success_url(self):
        next_page = self.request.GET.get("next")
        if next_page == "overview":
            return str(reverse("animal_overview"))
        return str(reverse("insemination_list"))


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
