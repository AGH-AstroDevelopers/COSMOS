import logging

import pytest

from src.telemetry_router_tool.processing.limits import are_limits_valid, load_limits

CATALOG = {
    "thermal.temperature": {"type": "number"},
    "thermal.heater": {"type": "boolean"},
    "power.voltage": {"type": "number"},
    "power.current": {"type": "number"},
}


def test_valid_limits_pass():
    limits = {
        "thermal.temperature": {"warning": {"low": 20, "high": 60}, "critical": {"low": 10, "high": 70}},
        "power.voltage": {"warning": {"low": 11.6}, "critical": {"low": 11.3}},
    }
    are_limits_valid("src", limits, CATALOG, [])  # must not raise


@pytest.mark.parametrize("limits, message", [
    ({"nope.x": {"warning": {"low": 1}}}, "not in the parameter catalog"),
    ({"thermal.heater": {"warning": {"low": 1}}}, "only for numbers"),
    ({"power.voltage": {"warning": {"low": 12, "high": 11}}}, "must be smaller than high"),
    ({"power.voltage": {"warning": {"low": 5, "high": 5}}}, "must be smaller than high"),
    ({"power.voltage": {"warning": {"low": 11.6}, "critical": {"low": 11.9}}}, "critical low"),
    ({"power.voltage": {"warning": {"high": 14}, "critical": {"high": 13}}}, "critical high"),
    ({"power.voltage": {"wrn": {"low": 1}}}, "unknown level"),
    ({"power.voltage": {"warning": {"min": 1}}}, "unknown bound"),
    ({"power.voltage": {"warning": {"low": "a"}}}, "must be a number"),
    ({"power.voltage": {"warning": {"low": True}}}, "must be a number"),
    ({"power.voltage": {"warning": {}}}, "needs at least one"),
])
def test_invalid_limits_raise(limits, message):
    with pytest.raises(ValueError, match=message):
        are_limits_valid("src", limits, CATALOG, [])


def test_all_problems_are_reported_together():
    limits = {
        "nope.x": {"warning": {"low": 1}},
        "power.voltage": {"warning": {"low": 12, "high": 11}},
    }
    with pytest.raises(ValueError) as error:
        are_limits_valid("src", limits, CATALOG, [])
    assert "nope.x" in str(error.value)
    assert "power.voltage" in str(error.value)


def test_missing_limits_only_warn_for_provided_numeric_parameters(caplog):
    limits = {"thermal.temperature": {"warning": {"high": 60}}}
    provided = ["thermal.temperature", "power.voltage", "thermal.heater"]
    with caplog.at_level(logging.WARNING):
        are_limits_valid("src", limits, CATALOG, provided)
    assert "power.voltage" in caplog.text            # numeric, provided, no limits
    assert "thermal.temperature" not in caplog.text  # has limits
    assert "thermal.heater" not in caplog.text       # not a number
    assert "power.current" not in caplog.text        # not provided by this source


def test_empty_limits_are_allowed():
    are_limits_valid("src", {}, CATALOG, ["power.voltage"])  # only warns, must not raise


def test_load_limits_reads_utf8_json(tmp_path):
    path = tmp_path / "status_limits.json"
    path.write_text('{"power.voltage": {"warning": {"low": 11.6}}}', encoding="utf-8")
    assert load_limits(path) == {"power.voltage": {"warning": {"low": 11.6}}}