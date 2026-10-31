# The logic in this file is specific to ONE source (the Python simulator).
# Every other source (e.g. hardware) will have its own version of this file.
# Only the output format is shared by all sources.

from src.telemetry_server.data_processing.flatten_catalog import get_catalog
from src.telemetry_server.data_processing.processor import make_entry

# (subsystem, parameter, section in the simulator packet, field in that section)
FIELD_MAP = [
    ("thermal", "temperature", "thermal",  "temperature_c"),
    ("power",   "voltage",     "power",    "voltage_v"),
    ("power",   "current",     "power",    "current_ma"),
    ("adcs",    "roll",        "attitude", "roll_deg"),
    ("adcs",    "pitch",       "attitude", "pitch_deg"),
    ("adcs",    "yaw",         "attitude", "yaw_deg"),
]

# Catalog keys of all parameters this source provides (used to warn about missing limits)
PROVIDED_KEYS = [f"{subsystem}.{parameter}" for subsystem, parameter, _, _ in FIELD_MAP]


def raw_to_catalog(packet: dict, limits: dict) -> dict:
    """Turn a (validated) simulator packet into dashboard-ready parameters:

        {"thermal.temperature": {"value", "unit", "status", "timestamp"}, ...}

    `limits` is the dict returned by the source's get_limits().
    If a source value needed a unit conversion (e.g. mA -> A), it would be done here.
    """
    catalog = get_catalog()
    params = {}
    for subsystem, parameter, section, field in FIELD_MAP:
        key = f"{subsystem}.{parameter}"
        entry = make_entry(key, packet[section][field], packet["timestamp"], catalog, limits)
        if entry:  # None means the parameter is not in the catalog
            params[key] = entry
    return params