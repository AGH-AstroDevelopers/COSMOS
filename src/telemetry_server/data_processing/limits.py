import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

LEVELS = ("warning", "critical")
BOUNDS = ("low", "high")


def load_limits(path: Path) -> dict:
    """Read a source's `status_limits.json` file (UTF-8) and return it as a dict."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def _is_number(value) -> bool:
    # bool is a subclass of int in Python, but True/False is not a valid limit
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def are_limits_valid(source_id: str, limits: dict, catalog: dict, provided_keys: list[str]) -> None:
    """Validate a source's limits once, at startup.

    Raises ValueError (listing ALL problems) if:
      - a key is not in the catalog, or the parameter is not a number,
      - a level or bound has an unknown name or a non-numeric value,
      - a level is empty, or "low" is not smaller than "high",
      - "critical" does not lie strictly outside "warning".

    Only logs a warning (no exception) for numeric parameters that the source
    provides but has no limits for: their status will be "unknown".
    """
    errors: list[str] = []

    for key, levels in limits.items():
        parameter = catalog.get(key)
        if parameter is None:
            errors.append(f"{key}: not in the parameter catalog")
            continue
        if parameter["type"] != "number":
            errors.append(f"{key}: limits make sense only for numbers (type is {parameter['type']})")
            continue

        for level, bounds in levels.items():
            if level not in LEVELS:
                errors.append(f"{key}: unknown level '{level}' (use {LEVELS})")
                continue
            if not bounds:
                errors.append(f"{key}.{level}: needs at least one of 'low' / 'high'")
                continue
            for name, value in bounds.items():
                if name not in BOUNDS:
                    errors.append(f"{key}.{level}: unknown bound '{name}' (use {BOUNDS})")
                elif not _is_number(value):
                    errors.append(f"{key}.{level}.{name}: must be a number, got {value!r}")
            low, high = bounds.get("low"), bounds.get("high")
            if _is_number(low) and _is_number(high) and low >= high:
                errors.append(f"{key}.{level}: low ({low}) must be smaller than high ({high})")

        warning, critical = levels.get("warning"), levels.get("critical")
        if warning and critical:
            w_low, c_low = warning.get("low"), critical.get("low")
            w_high, c_high = warning.get("high"), critical.get("high")
            if _is_number(w_low) and _is_number(c_low) and c_low >= w_low:
                errors.append(f"{key}: critical low ({c_low}) must be below warning low ({w_low})")
            if _is_number(w_high) and _is_number(c_high) and c_high <= w_high:
                errors.append(f"{key}: critical high ({c_high}) must be above warning high ({w_high})")

    if errors:
        raise ValueError(f"[{source_id}] invalid status limits:\n  - " + "\n  - ".join(errors))

    for key in provided_keys:
        parameter = catalog.get(key)
        if parameter and parameter["type"] == "number" and key not in limits:
            logger.warning("[%s] no limits for %s - its status will be 'unknown'", source_id, key)