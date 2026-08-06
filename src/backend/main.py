from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.backend.config import PORT
from src.backend.validator import validate_packet

app = FastAPI()
# Stores the most recently received telemetry packet in memory.
# Overwritten with every new packet. Lost on server restart.
latest_packet = None


# Endpoint to receive data from the simulator
# Requires a POST method and returns HTTP status 201 on success
@app.post("/telemetry", status_code=201)
async def receive_packet(data: dict):
    global latest_packet
    # "ok" if valid, else an error explanation
    validation_result = validate_packet(data)
    if validation_result == "ok":
        # if packet is valid -> store data and return status received
        latest_packet = data
        print(latest_packet)
        return {"status": "received"}
    else:
        # if packet is invalid -> return HTTP status 422 and error explanation
        return JSONResponse(status_code=422, content={"error": validation_result})
