"""
Kafka Manager Module

This module initializes a Kafka producer to send messages to a specified topic.
Messages are sent to random partitions within the topic.

Attributes:
    producer (Producer): The Confluent Kafka producer instance for sending
        messages.
"""

import json
import time
import random
from confluent_kafka import Producer, KafkaError

from src.config.logging import LoggingConfig
from src.config.kafka import KafkaConfig

logger = LoggingConfig.get_logger(__name__)

# Initialize Confluent Kafka producer
producer = Producer({
    'bootstrap.servers': KafkaConfig.KAFKA_BROKER
})

# Set a unique random seed for each instance (could use instance ID, time,
# or other unique factor)
random.seed(time.time())


def delivery_report(err, msg):
    """
    Callback function called when the message is delivered or fails.

    Args:
        err (KafkaError): The error, if any, that occurred on delivery.
        msg (Message): The message that was attempted to send.
    """
    if err is not None:
        logger.error("Message delivery failed: %s", err)
    else:
        logger.info("Message delivered to %s [%s]", msg.topic(),
                    msg.partition())


def send_message(message: dict) -> None:
    """
    Sends a message to a random partition in the Kafka topic.

    Args:
        message (dict): The message to send, in dictionary format.
    """
    # Convert message dictionary to a JSON string for sending
    message = json.dumps(message)

    # Choose a random partition from 0 to NUM_PARTITIONS - 1
    partition = random.randint(0, KafkaConfig.NUM_PARTITIONS - 1)

    try:
        # Send message to the randomly selected partition
        producer.produce(
            topic=KafkaConfig.KAFKA_TOPIC,
            value=message,
            partition=partition,
            callback=delivery_report
        )
        # Wait for the delivery report
        producer.poll(0)  # Triggers delivery report callbacks

    except BufferError as err:
        logger.error(
            "Local producer queue is full "
            "(%d messages awaiting delivery): %s",
            len(producer), err)
    except KafkaError as err:
        logger.error("Failed to send message: %s", err)
