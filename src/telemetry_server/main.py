"""Entry point of the telemetry serve, responsible for opening ports to sources and dashboards."""
import asyncio
import logging
import os
import socket
import sys
import uvicorn
from src.telemetry_server import config
from src.telemetry_server.communication.dashboards.hub import DashboardHub
from src.telemetry_server.communication.dashboards.server import create_dashboard_app
from src.telemetry_server.communication.sources.server import create_sources_app
from src.telemetry_server.communication.dispatcher import Dispatcher
from src.telemetry_server.data_processing.telemetry_source import TelemetrySource

#Create object for saving logs
logger = logging.getLogger(__name__)


def build_source(source_id: str) -> TelemetrySource:
    """Create the one telemetry source chosen by the user 
    (TODO: chosen in the launcher UI)."""
    try:
        source_class = config.AVAILABLE_SOURCES[source_id]
    except KeyError:
        raise ValueError(f"unknown source '{source_id}', available: {list(config.AVAILABLE_SOURCES)}") from None
    
    source = source_class()
    if source.id != source_id:
        raise ValueError(f"source '{source_id}' reports a different id '{source.id}'")
    return source

def port_is_free(host: str, port: int) -> bool:
    """Check whether the port is available on the given host address."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        #On non-Windows systems, enable SO_REUSEADDR to make it easier to reuse the port after previous TCP connections have been closed (TIME_WAIT)
        if os.name != "nt": 
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind((host, port))
        except OSError:
            return False
        return True


async def serve(server: uvicorn.Server, name: str) -> None:
    """Run one server; turn uvicorn's SystemExit (e.g. port taken) into a normal error."""
    try:
        await server.serve()
    except SystemExit:
        raise RuntimeError(f"{name} server could not start (port in use?)") from None

def create_connection(app, host: str, port: int) -> uvicorn.Server:
    """Configuration of one server connection(sources or dashboard)."""
    return uvicorn.Server(
        uvicorn.Config(
            app, 
            host=host, 
            port=port, 
            log_config=None, 
            access_log=False
        )
    )

async def connect(source_id:str, source: TelemetrySource) -> None:
    """Enables the source and dashboard ports. Core function for connecting whole tool logic."""
    hub = DashboardHub() # Object for managing connected dashboards
    dispatcher = Dispatcher(source_id, source, hub.enqueue_for_all_clients)  # decides what to do with data; hands results to the hub

    sources_connection = create_connection(
        create_sources_app(dispatcher), 
        config.SOURCE_HOST, 
        config.SOURCE_PORT)
    dashboard_connection = create_connection(
        create_dashboard_app(dispatcher, hub), 
        config.DASHBOARD_HOST, 
        config.DASHBOARD_PORT)

    logger.info("Telemetry server started: sources -> %s:%d, dashboards -> %s:%d",config.SOURCE_HOST, config.SOURCE_PORT, config.DASHBOARD_HOST, config.DASHBOARD_PORT)
    
    try:
        await asyncio.gather(
            serve(sources_connection, "Sources"),
            serve(dashboard_connection, "Dashboard"),
        )
    finally:
        logger.info("Telemetry server stopped")

def main(source_id: str = config.DEFAULT_SOURCE_ID) -> None: #TODO: take source_id from UI
    """Configure logging for Telemetry Server, create the chosen TelemetrySource from config.py, check if ports are free and run servers"""

    # TODO: replace with logging_setup.setup_logging() (next step)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    #Create the chosen source object
    try:
        source = build_source(source_id)
    except (ValueError, OSError) as error:
        logger.error("Cannot start: %s", error)
        sys.exit(1)

    #Check if ports are free
    for name, host, port in ( ("sources", config.SOURCE_HOST, config.SOURCE_PORT),
        ("dashboards", config.DASHBOARD_HOST, config.DASHBOARD_PORT)):
        if not port_is_free(host, port):
            logger.error("Cannot start: port %d (%s) is already in use. Close the program that uses it or change the port in config.py.", port, name)
            sys.exit(1)

    try:
        asyncio.run(connect(source_id,source))
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception:
        logger.exception("Telemetry server crashed")
        sys.exit(1)

if __name__ == "__main__":
    main()