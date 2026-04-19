from fastapi import FastAPI
from config import *

app = FastAPI()

latest_packet = {}


# Endpoint to receive data from the simulator
# Requires a POST method and returns HTTP status 201 on success
@app.post("/telemetry", status_code=201)
async def receive_packet(data: dict):
    global latest_packet
    latest_packet = data
    print(latest_packet)
    return {"status": "received"}
