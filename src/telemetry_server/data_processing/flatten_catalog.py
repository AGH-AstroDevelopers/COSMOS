import json
from functools import lru_cache
from pathlib import Path

PARAMETERS_CATALOG_PATH = Path(__file__).resolve().parent.parent / "parameters_catalog.json"
SUPPORTED_SCHEMA_VERSION = 1


def flatten_parameters_catalog(path: Path = PARAMETERS_CATALOG_PATH) -> dict[str, dict]:
    """Load the parameter catalog and flatten it for fast lookup.

    Shared by all sources (it is a helper for data processing).

    `parameters_catalog.json` is nested by subsystem, which is convenient for
    us (adding and maintaining parameters), but inconvenient to search in(dashboard). 
    
    Returns a dict keyed by `<subsystemId>.<parameterId>`, each value is the
    full definition of that parameter (name, type, unit, limits, ...).

    Raises ValueError if the schema version is unsupported or a parameter
    appears twice.
    """
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    version = data.get("schema_version")
    if version != SUPPORTED_SCHEMA_VERSION:
        raise ValueError(f"unsupported parameters.json schema_version: {version}")

    catalog: dict[str, dict] = {}
    for subsystem in data["subsystems"]:
        for parameter in subsystem["parameters"]:
            key = f"{subsystem['id']}.{parameter['id']}"
            if key in catalog:
                raise ValueError(f"duplicate parameter in parameters.json: {key}")
            catalog[key] = parameter
    return catalog


@lru_cache(maxsize=1)
def get_catalog() -> dict[str, dict]:
    """Return the flattened catalog, reading the file only once.

    The first call runs `flatten_parameters_catalog()` 
    Every later call returns the cached result until the program exits. """
    return flatten_parameters_catalog()