import logging

import pytest

from src.telemetry_router_tool.processing.processor import get_status, make_entry

VOLTAGE_LIMITS = {"warning": {"low": 11.6}, "critical": {"low": 11.3}}
TEMP_LIMITS = {"warning": {"low": 20, "high": 60}, "critical": {"low": 10, "high": 70}}


@pytest.mark.parametrize("value, expected", [
    (12.1, "ok"),
    (11.6, "ok"),         # equal to the limit is still fine (strict comparison)
    (11.5, "warning"),
    (11.3, "warning"),    # equal to the critical limit is only a warning
    (11.2, "critical"),
])
def test_status_with_only_low_limits(value, expected):
    assert get_status(value, VOLTAGE_LIMITS) == expected


@pytest.mark.parametrize("value, expected", [
    (35, "ok"),
    (20, "ok"), (60, "ok"),
    (61, "warning"), (70, "warning"),
    (71, "critical"),
    (19, "warning"), (10, "warning"),
    (9, "critical"),
])
def test_status_with_low_and_high_limits(value, expected):
    assert get_status(value, TEMP_LIMITS) == expected


def test_status_with_only_warning_level():
    assert get_status(65, {"warning": {"low": 20, "high": 60}}) == "warning"


@pytest.mark.parametrize("limits", [None, {}])
def test_status_without_limits_is_unknown(limits):
    assert get_status(12.1, limits) == "unknown"


CATALOG = {
    "power.voltage": {"type": "number", "unit": "V"},
    "thermal.heater": {"type": "boolean"},
}


def test_make_entry_for_number():
    entry = make_entry("power.voltage", 11.5, "2026-01-01T00:00:00+00:00", CATALOG,
                       {"power.voltage": VOLTAGE_LIMITS})
    assert entry == {
        "value": 11.5,
        "unit": "V",
        "status": "warning",
        "timestamp": "2026-01-01T00:00:00+00:00",
    }


def test_make_entry_for_number_without_limits_is_unknown():
    entry = make_entry("power.voltage", 11.5, "t", CATALOG, {})
    assert entry["status"] == "unknown"


def test_make_entry_for_boolean_has_no_status_and_no_unit():
    entry = make_entry("thermal.heater", True, "t", CATALOG, {})
    assert entry["status"] is None
    assert entry["unit"] is None


def test_make_entry_for_unknown_parameter_returns_none_and_warns(caplog):
    with caplog.at_level(logging.WARNING):
        assert make_entry("nope.x", 1, "t", CATALOG, {}) is None
    assert "nope.x" in caplog.text