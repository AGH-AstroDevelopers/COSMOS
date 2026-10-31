# Temperature (thermal subsystem), degrees Celsius
MIN_TEMP = 10.0
MAX_TEMP = 80.0
MAX_TEMP_DRIFT = 0.5 # max change per step

# Bus voltage (power subsystem), volts
MIN_VOLTAGE = 11.0
MAX_VOLTAGE = 13.0
MAX_VOLTAGE_DRIFT = 0.2 # max change per step

# Attitude angles roll / pitch / yaw (ADCS subsystem), degrees
MIN_DEG = -180.0
MAX_DEG = 180.0
MAX_DEG_DRIFT = 5.0 # max change per step

# Current draw (power subsystem), milliamperes
MIN_CURRENT = 100.0
MAX_CURRENT = 2000.0
MAX_CURRENT_DRIFT = 5.0 # max change per step

# Number of decimal places the simulator rounds values to
DECIMAL_PRECISION = 2