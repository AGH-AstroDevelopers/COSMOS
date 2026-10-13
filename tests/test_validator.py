from src.backend.validator import validate_packet

"""
Unit tests for the telemetry packet validator.
This module verifies that the validation logic correctly 
rejects invalid packets (missing fields, wrong types, out-of-bound values)
"""


def valid_packet():
    """
        Returns valid telemetry packet for each test
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
    """Fully valid packet should return 'ok'"""
    packet = valid_packet()
    assert validate_packet(packet) == "ok"


def test_validate_missing_fields():
    """Test that removing a required main dictionary key results in an error"""
    packet = valid_packet()
    del packet["power"]
    assert validate_packet(packet) == "missing field: power"


def test_validate_missing_nested_fields():
    """Test that removing a required nested key results in an error"""
    packet = valid_packet()
    del packet["attitude"]["yaw_deg"]
    assert validate_packet(packet) == "missing field: yaw_deg"


def test_validate_empty_packet():
    """Test that empty packet is rejected"""
    assert validate_packet({}) == "packet is empty"


def test_validate_packet_invalid_type():
    """Test that passing a string instead of a number triggers a type error"""
    packet = valid_packet()
    packet["thermal"]["temperature_c"] = "12"
    assert validate_packet(packet) == "invalid type: temperature_c must be a number"


def test_validate_packet_out_of_bounds():
    """Test that sensor values exceeding predefined limits are rejected"""
    packet = valid_packet()
    packet["thermal"]["temperature_c"] = 800
    assert validate_packet(packet) == "value out of range: temperature_c"
