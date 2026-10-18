import pytest
from datetime import datetime, timezone
from src.telemetry_router_tool.telemetry_source import TelemetrySource
from src.telemetry_router_tool.sources_adapters.python_simulator_v1.source_main import PythonSimulatorV1Source

"""
Unit tests for telemetry sources.
Tests that TelemetrySource subclasses adhere to the interface contract
and correctly decode or reject packets.
"""


def valid_packet():
    return {
        "packet_id": "a3f1c",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "simulator",
        "thermal": {"temperature_c": 23.4},
        "power": {"voltage_v": 12.1, "current_ma": 480.0},
        "attitude": {"roll_deg": 1.2, "pitch_deg": -0.4, "yaw_deg": 0.0}
    }


def test_python_simulator_v1_source_valid():
    source = PythonSimulatorV1Source()
    assert isinstance(source, TelemetrySource)
    assert source.id == "python_simulator_v1"
    assert source.name == "Python Simulator V1"

    packet = valid_packet()
    decoded = source.decode(packet)
    assert decoded["thermal.temperature"]["value"] == packet["thermal"]["temperature_c"]


def test_python_simulator_v1_source_invalid():
    source = PythonSimulatorV1Source()
    bad_packet = valid_packet()
    del bad_packet["thermal"]

    with pytest.raises(ValueError, match="missing field: thermal"):
        source.decode(bad_packet)


def test_python_simulator_v1_send_command():
    source = PythonSimulatorV1Source()
    with pytest.raises(NotImplementedError):
        source.send_command({"cmd": "ping"})
