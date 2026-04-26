"""utils/config_loader.py — Loads and validates config.yaml"""

import yaml
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
_cache = None


def load_config() -> dict:
    global _cache
    if _cache is None:
        with open(_CONFIG_PATH, "r") as f:
            _cache = yaml.safe_load(f)
    return _cache


def get(key_path: str, default=None):
    """Dot-notation access. e.g. get('business.currency') → '₹'"""
    cfg = load_config()
    keys = key_path.split(".")
    val = cfg
    for k in keys:
        if not isinstance(val, dict):
            return default
        val = val.get(k, default)
    return val
