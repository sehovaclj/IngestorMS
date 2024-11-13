"""
Configures the MQTT broker using environment variables.

Reads from a `.env` file to set MQTT connection parameters.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class MqttConfig:
    """
    Configuration class for MQTT settings.

    This class loads the MQTT broker configuration from environment variables.
    """
    BROKER = os.getenv('BROKER')
    PORT = int(os.getenv('PORT'))
    SHARED_TOPIC_METRICS = os.getenv('SHARED_TOPIC_METRICS')
    SHARED_TOPIC_SHUTDOWN = os.getenv('SHARED_TOPIC_SHUTDOWN')
