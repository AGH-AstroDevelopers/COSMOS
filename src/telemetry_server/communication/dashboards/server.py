from fastapi import FastAPI, WebSocket
from src.telemetry_server.communication.dashboards.hub import DashboardHub
from src.telemetry_server.communication.dispatcher import Dispatcher

def create_dashboard_app(dispatcher: Dispatcher, hub: DashboardHub) -> FastAPI:
    """The door for dashboards: they connect here and receive live data."""
    app = FastAPI(title="Telemetry server: dashboards")

    @app.get("/dashboard_port_health")
    async def health() -> dict:
        return {"status": "ok", "dashboards": hub.count_dashboards()}

    @app.websocket("/ws/connect")
    async def register_dashboard(websocket: WebSocket) -> None:
        """Register one dashboard, tell it which source is selected and manage its connection."""
        await hub.handle(websocket, initial_message=dispatcher.status_message)


    return app