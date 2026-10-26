import logging
from collections.abc import Callable
from src.telemetry_server.processing.telemetry_source import TelemetrySource

logger = logging.getLogger(__name__)

class Dispatcher:
    """The middle of the telemetry server: decides what happens with incoming data.

    NOTE: Must be called from the event loop thread (a background thread has to hand
    its data over with `loop.call_soon_threadsafe`).
    """

    def __init__(self, source_id:str, source: TelemetrySource, publish: Callable[[dict], None]):
        self._source_id=source_id
        self._source = source
        self._publish = publish
        self._last_message: dict | None = None

    @property
    def last_message(self) -> dict | None:
        return self._last_message

    @property
    def source_id(self) -> str:
        return self._source_id

    def handle_raw(self, raw: dict) -> dict:
        """Convert a raw packet from the given source and hand the result to `publish`.

        Returns the message that was published:
        `{"type": "telemetry", "source": <source id>, "data": {...}}`

        ValueError: if the source rejects the packet (nothing published)
        """
        ready_data = self._source.decode(raw)  # raises ValueError for an invalid packet
        message = {"type": "telemetry", "source": self._source_id, "data": ready_data}
        self._last_message = message
        self._publish(message)
        return message