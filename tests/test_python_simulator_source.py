import pytest

from src.sources.python_telemetry_simulator.simulator import generate_data
from src.telemetry_router_tool.sources_adapters.python_simulator_v1.data_processing import PROVIDED_KEYS, raw_to_catalog
from src.telemetry_router_tool.sources_adapters.python_simulator_v1.source_main import PythonSimulatorV1Source

EXPECTED_KEYS = {
    "thermal.temperature", "power.voltage", "power.current",
    "adcs.roll", "adcs.pitch", "adcs.yaw",
}


@pytest.fixture
def source():
    return PythonSimulatorV1Source()


def make_packet(temperature=23.4, voltage=12.1):
    """A hand-made packet. It is NOT validated: raw_to_catalog() trusts its input."""
    return {
        "timestamp": "2026-01-01T00:00:00+00:00",
        "thermal": {"temperature_c": temperature},
        "power": {"voltage_v": voltage, "current_ma": 540.0},
        "attitude": {"roll_deg": 1.2, "pitch_deg": -0.4, "yaw_deg": 3.0},
    }


def test_decode_returns_exactly_the_expected_parameters(source):
    assert set(source.decode(generate_data())) == EXPECTED_KEYS
    assert set(PROVIDED_KEYS) == EXPECTED_KEYS


def test_every_entry_has_the_four_dashboard_fields(source):
    for entry in source.decode(generate_data()).values():
        assert set(entry) == {"value", "unit", "status", "timestamp"}
        assert entry["status"] in {"ok", "warning", "critical", "unknown"}


def test_units_come_from_the_catalog(source):
    params = source.decode(generate_data())
    assert params["thermal.temperature"]["unit"] == "°C"
    assert params["power.voltage"]["unit"] == "V"
    assert params["power.current"]["unit"] == "mA"
    assert params["adcs.roll"]["unit"] == "°"


def test_values_are_copied_from_the_right_fields():
    params = raw_to_catalog(make_packet(temperature=23.4, voltage=12.1), {})
    assert params["thermal.temperature"]["value"] == 23.4
    assert params["power.voltage"]["value"] == 12.1
    assert params["power.current"]["value"] == 540.0
    assert params["adcs.pitch"]["value"] == -0.4


@pytest.mark.parametrize("temperature, voltage, temp_status, volt_status", [
    (23.4, 12.1, "ok", "ok"),
    (70.0, 11.5, "warning", "warning"),
    (10.0, 11.0, "warning", "critical"),
])
def test_statuses_follow_status_limits_json(source, temperature, voltage, temp_status, volt_status):
    params = raw_to_catalog(make_packet(temperature, voltage), source.get_limits())
    assert params["thermal.temperature"]["status"] == temp_status
    assert params["power.voltage"]["status"] == volt_status


def test_parameters_without_limits_are_unknown_but_still_sent(source):
    params = raw_to_catalog(make_packet(), source.get_limits())
    assert params["power.current"]["status"] == "unknown"
    assert params["adcs.roll"]["value"] == 1.2


def test_invalid_packet_raises_value_error(source):
    packet = generate_data()
    del packet["power"]
    with pytest.raises(ValueError):
        source.decode(packet)
    with pytest.raises(ValueError):
        source.decode({})


def test_broken_limits_file_stops_the_source_at_startup(tmp_path):
    path = tmp_path / "status_limits.json"
    path.write_text('{"power.voltage": {"warning": {"low": 12, "high": 11}}}', encoding="utf-8")
    with pytest.raises(ValueError, match="invalid status limits"):
        PythonSimulatorV1Source(limits_path=path)