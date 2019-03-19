from kafka import KafkaProducer, KafkaConsumer
from db import write_character
import time
import json

# Function that takes in a Dictionary, and converts it to a Byte string
def dump(message: dict) -> bytes:
    """
    Takes in DICT and convers to byte string
    Args: message
    Returns: json.dumps
    """
    return json.dumps(message).encode("utf8")


# Function that loads in Byte string, and convers it to JSON object
def load(message: bytes) -> dict:
    """
    Takes in byte string message, and converts it to dictionary / json
    Args: message
    Returns: JSON object
    """
    if message is None:
        return None
    else:
        return json.loads(message.decode("utf8"))


# Trying to produce Character output to Kafka topic
def kafka_produce(json):
    """
    Kafka producer, takes in JSON object, and publishes it to defined Kafka server
    Args: JSON
    Returns: nothing
    """
    producer = KafkaProducer(value_serializer=dump, bootstrap_servers="10.203.3.9:9092")
    producer.send("test", json)
    producer.flush()
    return


# Trying to consume from Kafka:
def kafka_consume():
    """
    Kafka consumer, takes in Kafka topic, and reads the latest items
    Args: none
    Returns: nothing
    """
    consumer = KafkaConsumer(
        "test",
        value_deserializer=load,
        bootstrap_servers="10.203.3.9:9092",
        group_id="testing",
    )
    time.sleep(1)
    for msg in consumer:
        print("Taking in Kafka character")
        write_character(msg.value)
        print("Written character to DB")
