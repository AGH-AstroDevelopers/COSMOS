import json
import time
from datetime import datetime
from random import uniform
from uuid import uuid4

# --- Configuration Constants ---

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
DECIMAL_PRECISION = 2

cur_params = {
    "temperature_c": uniform(MIN_TEMP, MAX_TEMP),
    "voltage_v": uniform(MIN_VOLTAGE, MAX_VOLTAGE),
    "current_ma": uniform(MIN_CURRENT, MAX_CURRENT),
    "roll_deg": 0.0,
    "pitch_deg": 0.0,
    "yaw_deg": 0.0,

}


def update(val, drift, v_min, v_max):
    return max(v_min, min(v_max, val + uniform(-drift, drift)))


def update_params():
    """
    Simulates physical sensor drift by applying a random walk to
    each parameter and clamping the results within realistic bounds.
    """

    cur_params["temperature_c"] = update(cur_params["temperature_c"], MAX_TEMP_DRIFT, MIN_TEMP, MAX_TEMP)

    cur_params["voltage_v"] = update(cur_params["voltage_v"], MAX_VOLTAGE_DRIFT, MIN_VOLTAGE, MAX_VOLTAGE)
    cur_params["current_ma"] = update(cur_params["current_ma"], MAX_CURRENT_DRIFT, MIN_CURRENT, MAX_CURRENT)

    cur_params["roll_deg"] = update(cur_params["roll_deg"], MAX_DEG_DRIFT, MIN_DEG, MAX_DEG)
    cur_params["pitch_deg"] = update(cur_params["pitch_deg"], MAX_DEG_DRIFT, MIN_DEG, MAX_DEG)
    cur_params["yaw_deg"] = update(cur_params["yaw_deg"], MAX_DEG_DRIFT, MIN_DEG, MAX_DEG)


def generate_data():
    update_params()
    state = {
        "packet_id": str(uuid4()),
        "timestamp": datetime.now().isoformat(),
        "source": "simulator",
        "thermal": {
            "temperature_c": round(cur_params["temperature_c"], DECIMAL_PRECISION)
        },
        "power": {
            "voltage_v": round(cur_params["voltage_v"], DECIMAL_PRECISION),
            "current_ma": round(cur_params["current_ma"], DECIMAL_PRECISION)
        },
        "attitude": {
            "roll_deg": round(cur_params["roll_deg"], DECIMAL_PRECISION),
            "pitch_deg": round(cur_params["pitch_deg"], DECIMAL_PRECISION),
            "yaw_deg": round(cur_params["yaw_deg"], DECIMAL_PRECISION)
        }
    }

    return json.dumps(state)


if __name__ == "__main__":
    try:
        while True:
            json_data = generate_data()
            print(json_data)
            time.sleep(1)
    except KeyboardInterrupt:
        # Log shutdown on Ctrl+C
        print("\n Data generation interrupted.")
    except Exception as e:
        # Log unexpected errors
        print(f"\n An unexpected error occurred: {e}")
