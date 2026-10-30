import logging
from collections.abc import Callable
from src.telemetry_server.data_processing.telemetry_source import TelemetrySource

logger = logging.getLogger(__name__)

class Dispatcher:
    """The middle of the telemetry server: decides what happens with incoming data.

    NOTE: Must be called from the event loop thread (a background thread has to hand
    its data over with `loop.call_soon_threadsafe`).
    """

    def __init__(self, source_id: str, source: TelemetrySource, publish: Callable[[dict], None]):
        self._source_id = source_id
        self._source = source
        self._publish = publish

    @property
    def status_message(self) -> dict:
        """Tells a dashboard which source this server is connected to (sent on connect)."""
        return {"type": "status", "source": self._source_id}

    @property
    def source_id(self) -> str:
        return self._source_id

    def handle_raw(self, raw: dict) -> dict:
        """Convert a raw packet from the source and hand the result to `publish`.

        Returns the message that was published: `{"type": "telemetry", "source": <source id>, "data": {...}}`
        ValueError: if the source rejects the packet (nothing published)
        """
        ready_data = self._source.decode(raw)  # raises ValueError for an invalid packet
        message = {"type": "telemetry", "source": self._source_id, "data": ready_data}
        self._publish(message)
        return message