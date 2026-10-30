from src.telemetry_server.data_processing.telemetry_source import TelemetrySource
from src.telemetry_server.data_processing.sources_adapters.python_simulator_v1.source_main import PythonSimulatorV1Source


#--------------Connection: SOURCE => TELEMETRY_SERVER config-----------------
SOURCE_PORT = 8081 # Port on which sources send their packets.
SOURCE_HOST = "0.0.0.0" #Determines where the server accepts connections: only from the same device or through all local IPv4 interfaces

REFRESH_INTERVAL = 1000 #Refresh interval for waiting for waiting for simulator data (in milliseconds)
DEFAULT_SOURCE_ID = "python_simulator_v1" 
AVAILABLE_SOURCES = {
    "python_simulator_v1": PythonSimulatorV1Source,
    # HardwareLoraSource,  # TODO
}

#--------------Connection: TELEMETRY_SERVER => DASHBOARD config-----------------
DASHBOARD_PORT = 8082 # Port on which dashboards connect (WebSocket for live data TODO: commands)
DASHBOARD_HOST = "0.0.0.0" 

# Pages allowed to call the server with HTTP requests from a browser
ALLOWED_ORIGINS = ["*"]

# How many messages may wait for one dashboard before the oldest ones are dropped(buffer)
DEFAULT_QUEUE_SIZE = 50

