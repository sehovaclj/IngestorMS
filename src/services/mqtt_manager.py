"""
This module provides MQTT functions for connection and message processing.
Messages are received as binary data,
unpacked into structured data, validated, and then publish to Kafka topics.
Configuration settings for logging, MQTT, and data validation are imported
from configuration modules.
"""

import json
import struct
from typing import Any, Optional
from paho.mqtt.client import Client, MQTTMessage

from src.config.logging import LoggingConfig
from src.config.mqtt import MqttConfig
from src.config.validation import DataValidationConfig
from src.utils.validation_utils import validate_data
from src.services.kafka_manager import send_message

# Configure the logger
logger = LoggingConfig.get_logger(__name__)


def on_connect(client: Client,
               _userdata: Any,
               _flags: dict,
               reason_code: int,
               _properties: Optional[dict] = None) -> None:
    """
    Handles the MQTT client's connection to the broker and subscribes to
    the shared topic.

    Args:
        client (Client): The MQTT client instance.
        reason_code (int): The connection result code (0 indicates success).
    """
    if reason_code == 0:
        logger.info("Connected to MQTT broker.")
        client.subscribe(MqttConfig.SHARED_TOPIC_METRICS)
        client.subscribe(MqttConfig.SHARED_TOPIC_SHUTDOWN)
    else:
        logger.error("Failed to connect to MQTT broker, return code %s",
                     reason_code)


# Callback function for when a message is received
def on_message(_client: Client,
               _userdata: Any,
               msg: MQTTMessage) -> None:
    """
    Processes incoming MQTT messages by ingesting the binary payload,
    unpacking it, validating the structured data, then publishing to a Kafka
    topic.

    Args:
        msg (MQTTMessage): The MQTT message object containing the payload.
    """
    # Log the topic of the message
    logger.info("Received message on topic: %s", msg.topic)

    # Step 1: Ingest the binary payload
    binary_data = msg.payload
    if len(binary_data) != DataValidationConfig.EXPECTED_BINARY_LENGTH:
        logger.error("Invalid binary data length: %s bytes",
                     len(binary_data))
        return

    # Step 2: Convert the binary data to JSON
    try:
        # unpack the data using struct.unpack
        unpacked_data = struct.unpack(DataValidationConfig.UNPACK_FORMAT,
                                      binary_data)  # Little-endian

        # Create a dictionary from the unpacked data
        data = {
            "battery_id": unpacked_data[0],
            "timestamp": unpacked_data[1],
            "voltage": unpacked_data[2],
            "current": unpacked_data[3],
            "temperature": unpacked_data[4],
            "state_of_charge": unpacked_data[5],
            "state_of_health": unpacked_data[6],
        }

        # Step 3: Validate the data
        # Validate data
        if validate_data(data):
            logger.info("Validated data: %s", json.dumps(data))
            send_message(data)
        else:
            logger.error("Validation failed for data: %s",
                         json.dumps(data))

    except struct.error as err:
        logger.error("Error unpacking binary data: %s", err)


def on_disconnect(_client: Client,
                  _userdata: Any,
                  reason_code: int,
                  _properties: Optional[dict] = None) -> None:
    """
    Handles disconnection from the MQTT broker, logging the result.

    Args:
        reason_code (int): The reason code for the disconnection
            (0 indicates a successful disconnect).
    """
    if reason_code == 0:
        logger.info("Successfully disconnected from MQTT broker.")
    else:
        logger.error(
            "Disconnected from MQTT broker with error, reason code: %s",
            reason_code)
