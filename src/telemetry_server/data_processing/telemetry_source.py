from abc import ABC, abstractmethod

class TelemetrySource(ABC):
    """Contract for every telemetry source (e.g. pythone simulator, hardware)"""

    id:str 
    name: str 

    @abstractmethod
    def decode(self, raw:dict) ->dict:
        """Validate the raw input and return dashboard-ready parameters:

            {"<subsystemId>.<parameterId>": {"value", "unit", "status", "timestamp"}, ...}

        Every source must return exactly this format, whatever its raw format is.
        Raises ValueError if the input is invalid.
        """

    @abstractmethod
    def get_limits(self) -> dict:
        """Return the alarm limits for this source (`status_limits.json`).

        Shared format, "low" and "high" are both optional:

            {"<subsystemId>.<parameterId>": {
                "warning":  {"low": 20, "high": 60},
                "critical": {"low": 10, "high": 70}}, ...}

        A parameter without an entry gets the status "unknown".
        An empty dict means that the source has no limits at all.
        """

    def send_command(self, command:dict) ->dict:
        """TODO: Sending command to the satellite (Uplink)"""
        raise NotImplementedError
