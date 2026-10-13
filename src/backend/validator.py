from datetime import datetime, timezone

MIN_TEMP = 10.0
MAX_TEMP = 80.0
MAX_TEMP_DRIFT = 0.5
MIN_VOLTAGE = 11.0
MAX_VOLTAGE = 13.0
MAX_VOLTAGE_DRIFT = 0.2
MAX_DEG = 180.0
MIN_DEG = -180.0
MAX_DEG_DRIFT = 5.0
MIN_CURRENT = 100.0
MAX_CURRENT = 2000.0
MAX_CURRENT_DRIFT = 5.0
DECIMAL_PRECISION = 2


def validate_packet(packet):
    """
    Validates the incoming telemetry data packet.

    This function checks if the provided packet meets all the required rules.

    :param packet:
    :return: str: "ok" if the packet is valid. If the validation fails,
             it returns a short error message explaining
             what went wrong (e.g., "missing field: thermal").
    """

    if not packet:
        return "packet is empty"

    # CHECK MISSING FIELDS

    # check main keys
    required_keys = ["packet_id", "timestamp", "source", "thermal", "power", "attitude"]
    for key in required_keys:
        if key not in packet:
            return f"missing field: {key}"

    thermal = packet["thermal"]
    power = packet["power"]
    attitude = packet["attitude"]

    # check that nested objects are dictionaries
    if not isinstance(thermal, dict):
        return "invalid type: thermal must be a dict"
    if not isinstance(power, dict):
        return "invalid type: power must be a dict"
    if not isinstance(attitude, dict):
        return "invalid type: attitude must be a dict"

    # check nested keys
    if "temperature_c" not in thermal:
        return "missing field: temperature_c"
    if "voltage_v" not in power:
        return "missing field: voltage_v"
    if "current_ma" not in power:
        return "missing field: current_ma"
    if "roll_deg" not in attitude:
        return "missing field: roll_deg"
    if "pitch_deg" not in attitude:
        return "missing field: pitch_deg"
    if "yaw_deg" not in attitude:
        return "missing field: yaw_deg"

    # check types
    if packet["packet_id"] == "":
        return "empty field: packet_id"
    number_fields = [
        ("roll_deg", attitude["roll_deg"]),
        ("pitch_deg", attitude["pitch_deg"]),
        ("yaw_deg", attitude["yaw_deg"]),
        ("current_ma", power["current_ma"]),
        ("voltage_v", power["voltage_v"]),
        ("temperature_c", thermal["temperature_c"])
    ]
    for field_name,val in number_fields:
        if not isinstance(val,(int, float)):
            return f"invalid type: {field_name} must be a number"

    # check ranges
    if not MIN_TEMP <= thermal["temperature_c"] <= MAX_TEMP:
        return "value out of range: temperature_c"
    if not MIN_VOLTAGE <= power["voltage_v"] <= MAX_VOLTAGE:
        return "value out of range: voltage_v"
    if not MIN_CURRENT <= power["current_ma"] <= MAX_CURRENT:
        return "value out of range: current_ma"
    if not MIN_DEG <= attitude["roll_deg"] <= MAX_DEG:
        return "value out of range: roll_deg"
    if not MIN_DEG <= attitude["pitch_deg"] <= MAX_DEG:
        return "value out of range: pitch_deg"
    if not MIN_DEG <= attitude["yaw_deg"] <= MAX_DEG:
        return "value out of range: yaw_deg"
    timestamp = datetime.fromisoformat(packet["timestamp"].replace("Z","+00:00"))
    if timestamp > datetime.now(timezone.utc):
        return "invalid timestamp: cannot be in the future"

    # all checks passed
    return "ok"
