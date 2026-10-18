from src.telemetry_router_tool.sources_adapters.python_simulator_v1.validator import is_packet_valid
from src.telemetry_router_tool.sources_adapters.python_simulator_v1.data_processing import to_readings
from src.telemetry_router_tool.telemetry_source import TelemetrySource

class PythonSimulatorV1Source(TelemetrySource):
    """Adapter for the Python simulator: validates the raw packet, then
    translates it into the internal format."""

    id="python_simulator_v1"
    name = "Python Simulator V1"

    def decode(self, raw:dict) -> dict:
        is_valid, error= is_packet_valid(raw)
        if is_valid is False:
            raise ValueError(error)
        return to_readings(raw)