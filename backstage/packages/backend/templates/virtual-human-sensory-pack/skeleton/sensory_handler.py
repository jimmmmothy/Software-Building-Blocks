import json
import logging

from dotenv import load_dotenv
import os

from services.extract_emotion import ExtractEmotion
from services.kafka.consumer import KafkaConsumer
from services.kafka.producer import KafkaProducer

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
REQUEST_TOPIC = os.getenv("KAFKA_REQUEST_TOPIC")
RESPONSE_TOPIC = os.getenv("KAFKA_RESPONSE_TOPIC")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")

extract_emotion = ExtractEmotion()
logger = logging.getLogger(__name__)


producer = KafkaProducer(BOOTSTRAP_SERVERS, REQUEST_TOPIC)


def convert_to_json(text: str) -> None | dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        logger.error("Invalid JSON format received: %s", text)
        return None
    return data


def process_query(text: str) -> None:
    data = convert_to_json(text)
    if not data:
        return

    user_query = data.get("user_query")
    if not user_query:
        logger.error("Missing 'user_query' field in message: %s", data)
        return

    try:
        current_mood = extract_emotion.get_emotion(user_query)
        logger.info("Emotion extracted: %s", current_mood)
        producer.send({
            "query": user_query,
            "emotion": current_mood
        })
    except Exception as e:
        logger.error(f"Error while extracting emotion: {e}", exc_info=True)


consumer = KafkaConsumer(BOOTSTRAP_SERVERS, RESPONSE_TOPIC, SCHEMA_REGISTRY_URL, message_handler=process_query)

def start_sensory_handler():
    consumer.start_listener()
