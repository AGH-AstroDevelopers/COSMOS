from src.telemetry_server.data_processing.sources_adapters.python_simulator_v1.validator import is_packet_valid
from src.telemetry_server.data_processing.telemetry_source import TelemetrySource

class PythonSimulatorV1Source(TelemetrySource):
    """Source for the Python simulator. Its packet format is already the
    internal one, so decode() only validates and passes the packet through."""

    id="python_simulator_v1"
    name = "Python Simulator V1"

    def decode(self, raw:dict) -> dict:
        is_valid, error= is_packet_valid(raw)
        if is_valid is False:
            raise ValueError(error)
        return raw