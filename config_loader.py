# config_loader.py
# Reads settings.cfg. Modernized 2024.
# Original hand-rolled because ConfigParser felt "too complicated" in 2013.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Parse settings.cfg and return a dict of known key/value pairs.

    Unknown keys are silently ignored (a typo in the file will never surface —
    this is a known limitation of the original design).
    Values containing '=' are handled correctly: only the first '=' is split on.
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return settings[key] as an int, or fallback if missing or not an integer."""
    try:
        return int(settings[key])
    except (KeyError, ValueError):
        return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Return settings[key], or fallback if the key is absent.

    Note: this is equivalent to settings.get(key, fallback).
    """
    return settings.get(key, fallback)
