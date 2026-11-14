import json

import pytest

from src.telemetry_router_tool.processing.flatten_catalog import flatten_parameters_catalog, get_catalog


def write_catalog(tmp_path, data):
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_flatten_builds_keys_from_subsystem_and_parameter(tmp_path):
    path = write_catalog(tmp_path, {
        "schema_version": 1,
        "subsystems": [
            {"id": "power", "parameters": [{"id": "voltage", "type": "number"}]},
            {"id": "thermal", "parameters": [{"id": "temperature", "type": "number"}]},
        ],
    })
    assert flatten_parameters_catalog(path) == {
        "power.voltage": {"id": "voltage", "type": "number"},
        "thermal.temperature": {"id": "temperature", "type": "number"},
    }


def test_unsupported_schema_version_is_rejected(tmp_path):
    path = write_catalog(tmp_path, {"schema_version": 99, "subsystems": []})
    with pytest.raises(ValueError, match="schema_version"):
        flatten_parameters_catalog(path)


def test_duplicate_parameter_is_rejected(tmp_path):
    path = write_catalog(tmp_path, {
        "schema_version": 1,
        "subsystems": [{"id": "power", "parameters": [{"id": "voltage"}, {"id": "voltage"}]}],
    })
    with pytest.raises(ValueError, match="duplicate"):
        flatten_parameters_catalog(path)


def test_real_catalog_loads_and_has_the_simulator_parameters():
    catalog = get_catalog()
    for key in ("thermal.temperature", "power.voltage", "power.current",
                "adcs.roll", "adcs.pitch", "adcs.yaw"):
        assert key in catalog


def test_real_catalog_has_no_limits_left():
    # Limits live in each source's status_limits.json, not in the catalog.
    leftovers = [key for key, parameter in get_catalog().items() if "limits" in parameter]
    assert leftovers == []