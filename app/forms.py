from django import forms
from .config import load_config


class AppSettingsForm(forms.Form):
    PREGNANCY_CHECK_OFFSET_DAYS = forms.IntegerField(min_value=0, label="Dias para verificação de prenhez")  # noqa
    REBREED_AFTER_BIRTH_DAYS = forms.IntegerField(min_value=0, label="Dias mínimos pós-parto para nova IA")  # noqa
    RECHECK_OR_REINSEMINATE_MIN_DAYS = forms.IntegerField(min_value=0, label="Dias mínimos para rechecagem/reinseminação")  # noqa
    UPCOMING_WINDOW_DAYS = forms.IntegerField(min_value=0, label="Janela de aviso (dias)")  # noqa
    GESTATION_DAYS = forms.IntegerField(min_value=0, label="Duração da gestação (dias)")  # noqa
    DRY_PERIOD_BEFORE_BIRTH_DAYS = forms.IntegerField(min_value=0, label="Dias de secagem antes do parto")  # noqa

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cfg = load_config()
        for name in self.fields:
            self.fields[name].initial = cfg.get(name)


class TaskReportForm(forms.Form):
    start_date = forms.DateField(label="Data inicial", widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    end_date = forms.DateField(label="Data final", widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))

    def clean(self):
        cleaned = super().clean()
        s = cleaned.get("start_date")
        e = cleaned.get("end_date")
        if s and e and s > e:
            raise forms.ValidationError("A data inicial não pode ser maior que a data final.")
        return cleaned
