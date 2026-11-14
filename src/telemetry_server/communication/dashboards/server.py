import logging
from pathlib import Path
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from src.telemetry_server import config
from src.telemetry_server.communication.dashboards.hub import DashboardHub
from src.telemetry_server.communication.dispatcher import Dispatcher

logger = logging.getLogger(__name__)

def create_dashboard_app(dispatcher: Dispatcher, hub: DashboardHub, build_dir: Path = config.DASHBOARD_BUILD_DIR) -> FastAPI:
    """The door for dashboards: they open the page here and receive live data."""
    app = FastAPI(title="Telemetry server: dashboards")

    @app.get("/dashboard_port_health")
    async def health() -> dict:
        return {"status": "ok", "dashboards": hub.count_dashboards()}

    @app.websocket("/ws/connect")
    async def register_dashboard(websocket: WebSocket) -> None:
        """Register one dashboard, tell it which source is selected and manage its connection."""
        await hub.handle(websocket, initial_message=dispatcher.status_message)

    # The built dashboard page (npm run build). It is added LAST, so the routes above keep priority
    # and everything else is served as a file. The page then connects back to this same address.
    if (build_dir / "index.html").is_file():
        app.mount("/", StaticFiles(directory=build_dir, html=True), name="dashboard")
    else:
        logger.warning("Dashboard is not built (%s not found): run `npm run build` in src/dashboard. "
                       "Data and WebSocket still work, but there is no page to open.", build_dir / "index.html")

    return app