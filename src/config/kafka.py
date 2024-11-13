"""
Configures the Kafka producer using environment variables.

Reads from a `.env` file to set Kafka producer parameters.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class KafkaConfig:
    """
    Configuration class for Kafka settings.

    This class loads the Kafka producer configuration from environment
    variables.
    """
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
    KAFKA_BROKER = os.getenv('KAFKA_BROKER')
    NUM_PARTITIONS = int(os.getenv('NUM_PARTITIONS'))
