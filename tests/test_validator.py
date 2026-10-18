from src.telemetry_router_tool.sources_adapters.python_simulator_v1.validator import is_packet_valid

"""
Unit tests for the telemetry packet validator.
This module verifies that the validation logic correctly 
accepts valid packets (returning True, "") and rejects invalid packets 
(returning False, error message) for missing fields, wrong types, out-of-bound values, etc.
"""


def valid_packet():
    """
    Returns a valid telemetry packet for testing.
    """
    return {
        "packet_id": "a3f1c",
        "timestamp": "2025-03-17T12:00:01Z",
        "source": "simulator",
        "thermal": {
            "temperature_c": 23.4
        },
        "power": {
            "voltage_v": 12.1,
            "current_ma": 480.0
        },
        "attitude": {
            "roll_deg": 1.2,
            "pitch_deg": -0.4,
            "yaw_deg": 0.0
        }
    }


def test_validate_valid_packet():
    """Fully valid packet should return (True, '')"""
    packet = valid_packet()
    is_valid, error = is_packet_valid(packet)
    assert is_valid is True
    assert error == ""


def test_validate_missing_fields():
    """Test that removing a required main dictionary key results in (False, 'missing field: <key>')"""
    packet = valid_packet()
    del packet["power"]
    is_valid, error = is_packet_valid(packet)
    assert is_valid is False
    assert error == "missing field: power"


def test_validate_missing_nested_fields():
    """Test that removing a required nested key results in (False, 'missing field: <key>')"""
    packet = valid_packet()
    del packet["attitude"]["yaw_deg"]
    is_valid, error = is_packet_valid(packet)
    assert is_valid is False
    assert error == "missing field: yaw_deg"


def test_validate_empty_packet():
    """Test that empty packet is rejected with (False, 'packet is empty')"""
    is_valid, error = is_packet_valid({})
    assert is_valid is False
    assert error == "packet is empty"


def test_validate_packet_invalid_type():
    """Test that passing a non-number triggers a type error"""
    packet = valid_packet()
    packet["thermal"]["temperature_c"] = "12"
    is_valid, error = is_packet_valid(packet)
    assert is_valid is False
    assert error == "invalid type: temperature_c must be a number"


def test_validate_packet_out_of_bounds():
    """Test that sensor values exceeding predefined limits are rejected"""
    packet = valid_packet()
    packet["thermal"]["temperature_c"] = 800
    is_valid, error = is_packet_valid(packet)
    assert is_valid is False
    assert error == "value out of range: temperature_c"


def test_validate_packet_empty_id():
    """Test that empty packet_id is rejected"""
    packet = valid_packet()
    packet["packet_id"] = ""
    is_valid, error = is_packet_valid(packet)
    assert is_valid is False
    assert error == "empty field: packet_id"


def test_validate_packet_future_timestamp():
    """Test that timestamp far in the future is rejected"""
    packet = valid_packet()
    packet["timestamp"] = "2099-01-01T00:00:00Z"
    is_valid, error = is_packet_valid(packet)
    assert is_valid is False
    assert error == "invalid timestamp: cannot be in the future"

