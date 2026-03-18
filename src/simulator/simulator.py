import json
import time
from datetime import datetime
from random import uniform
from uuid import uuid4

MIN_TEMP = 10.0
MAX_TEMP = 80.0
MAX_TEMP_DRIFT = 0.5
MIN_VOLTAGE = 11.0
MAX_VOLTAGE = 13.0
MAX_VOLTAGE_DRIFT = 0.2
MAX_DEG = 180.0
MIN_DEG = -180.0
MAX_DEG_DRIFT = 5.0
MIN_CURRENT = 100.0
MAX_CURRENT = 2000.0
MAX_CURRENT_DRIFT = 5.0

cur_params = {
    "temperature_c": uniform(MIN_TEMP, MAX_TEMP),
    "voltage_v": uniform(MIN_VOLTAGE, MAX_VOLTAGE),
    "current_ma": uniform(MIN_CURRENT, MAX_CURRENT),
    "roll_deg": 0.0,
    "pitch_deg": 0.0,
    "yaw_deg": 0.0,

}


def update_params():
    # TODO: changing and checking parameters
    pass


def generate_data():
    update_params()
    state = {
        "packet_id": str(uuid4()),
        "timestamp": datetime.now().isoformat(),
        "source": "simulator",
        "thermal": {
            "temperature_c": cur_params["temperature_c"]
        },
        "power": {
            "voltage_v": cur_params["voltage_v"],
            "current_ma": cur_params["current_ma"]
        },
        "altitude": {
            "roll_deg": cur_params["roll_deg"],
            "pitch_deg": cur_params["pitch_deg"],
            "yaw_deg": cur_params["yaw_deg"]
        }
    }

    return json.dumps(state)


if __name__ == "__main__":
    # TODO: exception handling
    while True:
        json_data = generate_data()
        print(json_data)
        time.sleep(1)
