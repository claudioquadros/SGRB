# app/mixins.py
from django.shortcuts import redirect
from django.urls import reverse


class NextRedirectMixin:
    """
    Mixin que redireciona para a URL 'next' mantendo os filtros
    da query string.
    Exemplo:
    /animals/create/?next=animal_list&farm=2&name=Branca
    -> retorna para /animals/?farm=2&name=Branca
    """

    def get_next_url(self, default_view):
        next_view = self.request.GET.get("next", default_view)
        filters = self.request.GET.urlencode()

        # Remove parâmetros que não precisamos manter
        params = "&".join(
            p for p in filters.split("&") if not p.startswith(("next=", "csrfmiddlewaretoken="))  # noqa
        )

        url = reverse(next_view)
        if params:
            return f"{url}?{params}"
        return url

    def form_valid(self, form):
        """
        Sobrescreve o comportamento padrão das Create/Update Views.
        Salva o formulário e redireciona para a URL 'next', mantendo os
        filtros.
        """
        self.object = form.save()
        return redirect(self.get_next_url(self.success_url))

    def get_initial(self):
        initial = super().get_initial() if hasattr(super(), 'get_initial') else {}  # noqa
        farm_id = self.request.GET.get('farm')
        if farm_id:
            initial['farm'] = farm_id
        return initial
