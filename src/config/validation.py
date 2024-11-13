"""
This module defines the DataValidationConfig class, which provides
configuration for validating battery parameters in an IoT setting.

Each attribute in the class represents a parameter with its expected
data type and permissible range of values for validation purposes.
Additionally, the module specifies the expected binary length for data
payloads and the unpack format, ensuring consistent data structure
interpretation across the system.
"""


class DataValidationConfig:
    """Configuration for data validation of expected binary length, battery
    parameters, and unpack format."""
    EXPECTED_BINARY_LENGTH = 17

    # Assuming the binary format matches the BatteryData struct in C:
    # - uint8_t battery_id (1 byte)
    # - int64_t timestamp (8 bytes)
    # - uint16_t voltage (2 bytes)
    # - uint16_t current (2 bytes)
    # - int16_t temperature (2 bytes)
    # - uint8_t state_of_charge (1 byte)
    # - uint8_t state_of_health (1 byte)
    UNPACK_FORMAT = "<BqHHhBB"  # little-endian

    BATTERY_ID = {"type": int}
    TIMESTAMP = {"type": int}
    VOLTAGE = {"type": int, "min": 0, "max": 600}
    CURRENT = {"type": int, "min": 0, "max": 200}
    TEMPERATURE = {"type": int, "min": -100, "max": 1000}
    STATE_OF_CHARGE = {"type": int, "min": 0, "max": 100}
    STATE_OF_HEALTH = {"type": int, "min": 0, "max": 100}
