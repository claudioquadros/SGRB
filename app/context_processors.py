from typing import Optional # noqa


def selected_farm(request):
    """
    Injecta a fazenda selecionada na sessão, se existir.
    Disponibiliza selected_farm_id e selected_farm no template.
    """
    farm = None
    farm_id = request.session.get('selected_farm_id')
    if farm_id:
        try:
            from farms.models import Farm
            farm = Farm.objects.filter(pk=farm_id).first()
        except Exception:
            farm = None
    return {
        'selected_farm_id': farm_id,
        'selected_farm': farm,
    }
