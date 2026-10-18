# Maps the simulator packet layout to the internal parameter ids.
# (subsystemId, parameterId, packet section, key inside that section)
# subsystemId / parameterId must match the ids in the dashboard telemetryConfig
FIELD_MAP = [
    ("thermal", "temperature", "thermal", "temperature_c"),
    ("power", "voltage", "power", "voltage_v"),
    ("power", "current", "power", "current_ma"),
    ("adcs", "roll", "attitude", "roll_deg"),
    ("adcs", "pitch", "attitude", "pitch_deg"),
    ("adcs", "yaw", "attitude", "yaw_deg"),
]

def to_readings(packet: dict) -> dict:
    """Translate a VALIDATED simulator packet into the internal format.

    Keys are "<subsystemId>.<parameterId>". Units and alarm status are added
    later by the shared processor, because they do not depend on the source.
    """
    return {
        "timestamp": packet["timestamp"],
        "readings": {
            f"{subsystem_id}.{parameter_id}": packet[section][key]
            for subsystem_id, parameter_id, section, key in FIELD_MAP
        },
    }
