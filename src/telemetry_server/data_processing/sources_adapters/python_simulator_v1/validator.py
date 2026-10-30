from datetime import datetime, timezone

from src.sources.python_telemetry_simulator.valid_ranges import *

def is_packet_valid(packet: dict) -> tuple[bool, str]:
    """
    Validates the incoming telemetry data packet.
    Checks if the provided packet meets all schema, type, range, and timestamp rules.

    :param packet: Dictionary containing telemetry packet data
    :return: (True, "") if the packet is valid.
             (False, error_message) if validation fails.
    """
    if not packet:
        return False, "packet is empty"

    # ---------- CHECK MISSING FIELDS ----------
    # Main keys
    required_keys = ["packet_id", "timestamp", "source", "thermal", "power", "attitude"]
    for key in required_keys:
        if key not in packet:
            return False, f"missing field: {key}"

    # Nested objects must be dictionaries
    thermal = packet["thermal"]
    power = packet["power"]
    attitude = packet["attitude"]
    if not isinstance(thermal, dict):
        return False, "invalid type: thermal must be a dict"
    if not isinstance(power, dict):
        return False, "invalid type: power must be a dict"
    if not isinstance(attitude, dict):
        return False, "invalid type: attitude must be a dict"

    # Nested keys
    if "temperature_c" not in thermal:
        return False, "missing field: temperature_c"
    if "voltage_v" not in power:
        return False, "missing field: voltage_v"
    if "current_ma" not in power:
        return False, "missing field: current_ma"
    if "roll_deg" not in attitude:
        return False, "missing field: roll_deg"
    if "pitch_deg" not in attitude:
        return False, "missing field: pitch_deg"
    if "yaw_deg" not in attitude:
        return False, "missing field: yaw_deg"

    # Check packet_id
    if not packet["packet_id"]:
        return False, "empty field: packet_id"

    # Check numeric types
    number_fields = [
        ("roll_deg", attitude["roll_deg"]),
        ("pitch_deg", attitude["pitch_deg"]),
        ("yaw_deg", attitude["yaw_deg"]),
        ("current_ma", power["current_ma"]),
        ("voltage_v", power["voltage_v"]),
        ("temperature_c", thermal["temperature_c"]),
    ]
    for field_name, val in number_fields:
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            return False, f"invalid type: {field_name} must be a number"

    # Check ranges
    if not MIN_TEMP <= thermal["temperature_c"] <= MAX_TEMP:
        return False, "value out of range: temperature_c"
    if not MIN_VOLTAGE <= power["voltage_v"] <= MAX_VOLTAGE:
        return False, "value out of range: voltage_v"
    if not MIN_CURRENT <= power["current_ma"] <= MAX_CURRENT:
        return False, "value out of range: current_ma"
    if not MIN_DEG <= attitude["roll_deg"] <= MAX_DEG:
        return False, "value out of range: roll_deg"
    if not MIN_DEG <= attitude["pitch_deg"] <= MAX_DEG:
        return False, "value out of range: pitch_deg"
    if not MIN_DEG <= attitude["yaw_deg"] <= MAX_DEG:
        return False, "value out of range: yaw_deg"

    # Check timestamp format 
    try:
        ts_str = str(packet["timestamp"]).replace("Z", "+00:00")
        timestamp = datetime.fromisoformat(ts_str)
        if timestamp > datetime.now(timezone.utc):
            return False, "invalid timestamp: cannot be in the future"
    except (ValueError, TypeError):
        return False, "invalid timestamp format"

    return True, ""
