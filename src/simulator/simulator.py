import json
import time
from random import uniform
from uuid import uuid4
from datetime import datetime, timezone

import logging
import requests 
from config import BACKEND_URL, SEND_INTERVAL_S

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

#--------logger configs
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]: %(message)s"))

# logger file
file_handler = logging.FileHandler("simulator.log")
file_handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]: %(message)s"))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

#------------------


def update(val, drift, v_min, v_max):
    """
    Simulates sensor drift using a 'random walk' technique.
    
    (The value changes gradually by adding a small random step to the current state. 
    This mimics real-world physical sensors where values change continuously.)

    :param val: Current sensor value.
    :param drift: Maximum allowed change per step (step size).
    :param v_min: Minimum physical bound for the sensor.
    :param v_max: Maximum physical bound for the sensor.
    :return : Updated value clamped within [v_min, v_max].
    """
    return max(v_min, min(v_max, val + uniform(-drift, drift)))


def update_params():
    """
    Simulates physical sensor drift by applying a random walk to
    each parameter.
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
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

    return state 


def send_packet(packet:dict)->None:
    """Sends a telemetry packet to the backend via HTTP POST.
    - If the backend is unavailable, logs a warning and continues
    - Simulator never crashes due to network failure

    :param packet: The telemetry data dict to send as JSON."""
    try:
        response = requests.post(BACKEND_URL, json=packet, timeout=2) #No response after 2 sec-> error:timeout
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logger.warning(f"Backend unavailable at {BACKEND_URL}. Skipping send.")
    except requests.exceptions.Timeout:
        logger.warning(f"Request to {BACKEND_URL} timed out. Skipping send.")
    except  requests.exceptions.HTTPError as e:
        logger.warning(f"Backend returned an error: {e}. Skipping send.")
    except Exception as e:
        logger.error(f"Unexpected error while sending packet: {e}")


if __name__ == "__main__":
    # NOTE: This block ensures the script only runs when executed directly from
    # the terminal (e.g. python simulator.py), not when imported as a module by another file.
    try:
        while True:
            packet=generate_data()
            logger.info(json.dumps(packet))

            send_packet(packet)
            time.sleep(SEND_INTERVAL_S)
    except KeyboardInterrupt: # Log shutdown on Ctrl+C
        logger.info("Data generation interrupted.")
    except Exception as e: # Log unexpected errors
        logger.error(f"An unexpected error occurred: {e}")
