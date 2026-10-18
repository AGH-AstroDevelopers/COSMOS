from pathlib import Path

from src.telemetry_router_tool.processing.flatten_catalog import get_catalog
from src.telemetry_router_tool.processing.limits import are_limits_valid, load_limits
from src.telemetry_router_tool.sources_adapters.python_simulator_v1.data_processing import PROVIDED_KEYS, raw_to_catalog
from src.telemetry_router_tool.sources_adapters.python_simulator_v1.validator import is_packet_valid
from src.telemetry_router_tool.telemetry_source import TelemetrySource

# source_main.py -> parents[3] is `src/`
DEFAULT_LIMITS_PATH = Path(__file__).resolve().parents[3] / "sources" / "python_telemetry_simulator" / "status_limits.json"


class PythonSimulatorV1Source(TelemetrySource):
    """Adapter for the Python simulator (raw packet in, dashboard-ready parameters out).

    id:         identifier used to select this source in the router.
    name:       human-readable name.
    decode:     validates the raw packet and converts it to the catalog format.
    get_limits: alarm limits of this source (from its status_limits.json).
    """

    id = "python_simulator_v1"
    name = "Python Simulator V1"

    def __init__(self, limits_path: Path = DEFAULT_LIMITS_PATH):
        """Load and check if the limits are in correct format once."""
        self._limits = load_limits(limits_path)
        are_limits_valid(self.id, self._limits, get_catalog(), PROVIDED_KEYS)

    def get_limits(self) -> dict:
        return self._limits

    def decode(self, raw: dict) -> dict:
        """Validate the raw packet and convert it to the catalog format
        understood by the dashboard. Raises ValueError if the packet is invalid."""
        is_valid, error = is_packet_valid(raw)
        if not is_valid:
            raise ValueError(error)
        return raw_to_catalog(raw, self._limits)