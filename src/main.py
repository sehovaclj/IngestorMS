"""
This module is the entrypoint in which we start our mqtt client.
"""

from src.config.logging import LoggingConfig
from src.config.mqtt import MqttConfig
from src.services.mqtt_manager import start_mqtt

# Configure the logger
logger = LoggingConfig.get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting IngestorMS with CLIENT_ID: %s",
                MqttConfig.CLIENT_ID)
    start_mqtt()
