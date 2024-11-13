"""
This module initializes an MQTT client and starts a microservice to listen
to shared topics on the MQTT broker EMQX. Configuration settings for logging
and MQTT connection are imported from the respective config modules.
"""
import uuid

import paho.mqtt.client as mqtt

from src.config.logging import LoggingConfig
from src.config.mqtt import MqttConfig
from src.services.mqtt_manager import on_connect, on_message, on_disconnect

# Configure the logger
logger = LoggingConfig.get_logger(__name__)

# initialize the client id
CLIENT_ID = f"client_{uuid.uuid4()}"


def start_mqtt():
    """
    Connects to the MQTT broker and starts the MQTT client loop.

    Uses configuration settings from MqttConfig for broker address
    and port, then begins the loop to handle messages.
    """

    # MQTT client setup and connection

    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                         client_id=CLIENT_ID, protocol=mqtt.MQTTv311,
                         transport="tcp")

    # Setup MQTT callbacks and start loop
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # now connect and loop forever
    client.connect(MqttConfig.BROKER, MqttConfig.PORT)
    client.loop_forever()


if __name__ == "__main__":
    logger.info("Starting IngestorMS with CLIENT_ID: %s", CLIENT_ID)
    start_mqtt()
