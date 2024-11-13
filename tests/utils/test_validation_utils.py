"""
This module contains unit tests for the `validate_data` function in an IoT
setting. The tests validate that the data dictionary conforms to the
expected types and ranges specified in the `DataValidationConfig` class.

Each test uses the configurations directly from `DataValidationConfig` to
ensure that the function correctly accepts or rejects data based on the
specified limits.
"""

import pytest
from src.utils.validation_utils import validate_data
from src.config.validation import DataValidationConfig


@pytest.mark.data_validation
def test_validate_data_valid():
    """
    Tests that `validate_data` returns True for a valid data dictionary.

    The test provides values within the permissible ranges specified
    in `DataValidationConfig`. This test should pass if the validation
    logic correctly identifies the data as valid.
    """

    # Valid data dictionary that should pass validation
    valid_data = {
        "battery_id": 1,
        "timestamp": 1617954800,
        "voltage": (DataValidationConfig.VOLTAGE["max"] +
                    DataValidationConfig.VOLTAGE["min"]) // 2,
        "current": (DataValidationConfig.CURRENT["max"] +
                    DataValidationConfig.CURRENT["min"]) // 2,
        "temperature": (DataValidationConfig.TEMPERATURE["max"] +
                        DataValidationConfig.TEMPERATURE["min"]) // 2,
        "state_of_charge": (DataValidationConfig.STATE_OF_CHARGE["max"] +
                            DataValidationConfig.STATE_OF_CHARGE["min"]) // 2,
        "state_of_health": (DataValidationConfig.STATE_OF_HEALTH["max"] +
                            DataValidationConfig.STATE_OF_HEALTH["min"]) // 2,
    }
    assert validate_data(valid_data) is True


@pytest.mark.data_validation
def test_validate_data_invalid():
    """
    Tests that `validate_data` returns False for an invalid data dictionary.

    This test provides values outside the permissible ranges specified
    in `DataValidationConfig`, ensuring that the validation logic
    correctly identifies the data as invalid.
    """
    # Invalid data dictionary that should fail validation
    invalid_data = {
        "battery_id": 1,
        "timestamp": 1617954800,
        "voltage": DataValidationConfig.VOLTAGE["max"] + 100,
        # Exceeds max voltage
        "current": DataValidationConfig.CURRENT["max"] + 100,
        # Exceeds max current
        "temperature": DataValidationConfig.TEMPERATURE["min"] - 200,
        # Below min temperature
        "state_of_charge": DataValidationConfig.STATE_OF_CHARGE["max"] + 50,
        # Exceeds max state_of_charge
        "state_of_health": DataValidationConfig.STATE_OF_HEALTH["min"] - 10,
        # Below min state_of_health
    }
    assert validate_data(invalid_data) is False
