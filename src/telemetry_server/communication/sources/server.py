import logging
from fastapi import FastAPI, HTTPException
from src.telemetry_server.communication.dispatcher import Dispatcher

logger = logging.getLogger(__name__)

def create_sources_app(dispatcher: Dispatcher) -> FastAPI:
    """The door for the source that sends its data itself (e.g. the simulator).
    The source POSTs a raw packet; the dispatcher converts it and passes it on.
    """
    app = FastAPI(title="Telemetry server: sources")

    @app.get("/source_port_health")
    async def health() -> dict:
        return {"status": "ok", "source": dispatcher.source_id}

    # `async def` on purpose: the dispatcher and the hub must run on the same event
    # loop as the server. A plain `def` would run in a separate thread.
    @app.post("/telemetry_stream")
    async def telemetry_stream(raw: dict) -> dict:
        """Receive one raw packet.
        422 = the source rejected the packet."""
        try:
            message = dispatcher.handle_raw(raw)
        except ValueError as error:
            logger.warning("Rejected packet from %s: %s", dispatcher.source_id, error)
            raise HTTPException(status_code=422, detail=str(error))
        return {"status": "ok", "parameters": len(message["data"])}

    return app