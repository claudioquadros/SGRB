import json
from pathlib import Path
from django.conf import settings


DEFAULTS = {
    "PREGNANCY_CHECK_OFFSET_DAYS": 10,
    "REBREED_AFTER_BIRTH_DAYS": 40,
    "RECHECK_OR_REINSEMINATE_MIN_DAYS": 18,
    "UPCOMING_WINDOW_DAYS": 10,
    "GESTATION_DAYS": 282,
    "DRY_PERIOD_BEFORE_BIRTH_DAYS": 50,
}


CONFIG_FILENAME = "app_settings.json"


def _config_path() -> Path:
    base_dir = Path(getattr(settings, "BASE_DIR", "."))
    return base_dir / CONFIG_FILENAME


def load_config() -> dict:
    path = _config_path()
    if path.exists():
        try:
            return {**DEFAULTS, **json.loads(path.read_text(encoding="utf-8"))}
        except Exception:
            return DEFAULTS.copy()
    return DEFAULTS.copy()


def save_config(data: dict) -> None:
    path = _config_path()
    # only persist known keys as ints
    safe = {k: int(data.get(k, DEFAULTS[k])) for k in DEFAULTS.keys()}
    path.write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")  # noqa


def get_int(key: str, default: int) -> int:
    cfg = load_config()
    try:
        return int(cfg.get(key, default))
    except (TypeError, ValueError):
        return int(default)
