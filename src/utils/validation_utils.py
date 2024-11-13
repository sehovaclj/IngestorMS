"""
This module provides a utility function for validating battery data in an IoT
setting.

The validate_data function checks that the data dictionary conforms to
the expected types and ranges specified in the DataValidationConfig class.
"""

from typing import Dict, Any
from src.config.validation import DataValidationConfig


def validate_data(data: Dict[str, Any]) -> bool:
    """
    Validates battery data based on expected types and value ranges.

    Args:
        data (Dict[str, Any]): The data dictionary containing battery
        parameters to validate.

    Returns:
        bool: True if all parameters are valid, False otherwise.
    """
    try:
        checks = [
            isinstance(data["battery_id"],
                       DataValidationConfig.BATTERY_ID["type"]) and data[
                "battery_id"] >= 0,
            isinstance(data["timestamp"],
                       DataValidationConfig.TIMESTAMP["type"]) and data[
                "timestamp"] >= 0,
            isinstance(data["voltage"],
                       DataValidationConfig.VOLTAGE["type"]) and
            DataValidationConfig.VOLTAGE["min"] <= data["voltage"] <=
            DataValidationConfig.VOLTAGE["max"],
            isinstance(data["current"],
                       DataValidationConfig.CURRENT["type"]) and
            DataValidationConfig.CURRENT["min"] <= data["current"] <=
            DataValidationConfig.CURRENT["max"],
            isinstance(data["temperature"],
                       DataValidationConfig.TEMPERATURE["type"]) and
            DataValidationConfig.TEMPERATURE["min"] <= data["temperature"] <=
            DataValidationConfig.TEMPERATURE["max"],
            isinstance(data["state_of_charge"],
                       DataValidationConfig.STATE_OF_CHARGE["type"]) and
            DataValidationConfig.STATE_OF_CHARGE["min"] <= data[
                "state_of_charge"] <= DataValidationConfig.STATE_OF_CHARGE[
                "max"],
            isinstance(data["state_of_health"],
                       DataValidationConfig.STATE_OF_HEALTH["type"]) and
            DataValidationConfig.STATE_OF_HEALTH["min"] <= data[
                "state_of_health"] <= DataValidationConfig.STATE_OF_HEALTH[
                "max"],
        ]
        for check in checks:
            if check:
                continue
            return False
        return True
    except KeyError:
        return False
