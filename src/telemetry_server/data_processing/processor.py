import logging

logger = logging.getLogger(__name__)


def get_status(value: float, limits: dict | None) -> str:
    """Compare a numeric value with the alarm limits of ONE parameter.

    Returns "critical", "warning", "ok" or "unknown" (no limits were given).
    Critical is checked first, so a value outside both ranges is reported as
    critical. The boundaries are strict: a value equal to a limit is still fine
    (value < low, value > high).
    """
    if not limits:
        return "unknown"

    for level in ("critical", "warning"):
        bounds = limits.get(level)
        if not bounds:
            continue
        low = bounds.get("low")
        high = bounds.get("high")
        if low is not None and value < low:
            return level
        if high is not None and value > high:
            return level
    return "ok"


def make_entry(key: str, value, timestamp: str, catalog: dict, limits: dict) -> dict | None:
    """Build one dashboard-ready entry for a single parameter.

    Shared by all sources: the adapter finds the value in its own packet format,
    this function adds the unit (from the catalog) and the status (computed from
    the limits of the source: `limits` is the whole dict from get_limits()).

    Returns {"value", "unit", "status", "timestamp"}, or None if the parameter
    is not in the catalog (it is logged and the caller skips it).
    """
    parameter = catalog.get(key)
    if parameter is None:
        logger.warning("Unknown parameter %s - skipped", key)
        return None

    # Status only makes sense for numbers (booleans and enums have no limits).
    status = None
    if parameter["type"] == "number":
        status = get_status(value, limits.get(key))

    return {
        "value": value,
        "unit": parameter.get("unit"),
        "status": status,
        "timestamp": timestamp,
    }