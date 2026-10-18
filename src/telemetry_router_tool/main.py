from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.telemetry_router_tool.config import PORT
from src.telemetry_router_tool.sources_adapters.python_simulator_v1.validator import is_packet_valid

app = FastAPI()
# Stores the most recently received telemetry packet in memory.
# Overwritten with every new packet. Lost on server restart.
latest_packet = None


# Endpoint to receive data from the simulator
# Requires a POST method and returns HTTP status 201 on success
@app.post("/telemetry", status_code=201)
async def receive_packet(data: dict):
    global latest_packet
    is_valid, error = is_packet_valid(data)
    if is_valid:
        # if packet is valid -> store data and return status received
        latest_packet = data
        print(latest_packet)
        return {"status": "received"}
    else:
        # if packet is invalid -> return HTTP status 422 and error explanation
        return JSONResponse(status_code=422, content={"error": error})
