import threading
import logging
from confluent_kafka import Consumer, KafkaError


class KafkaConsumer:
    """
    Simple Kafka consumer that receives plain text messages and
    calls a user-provided message_handler for each message.
    """
    def __init__(self, bootstrap_servers, topic, group_id="default-group", message_handler=None):
        self.topic = topic
        self.message_handler = message_handler
        self.logger = logging.getLogger(__name__)

        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "latest",
        })

    def start_listener(self):
        """Start the Kafka listener in a separate daemon thread."""
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()
        self.logger.debug(f"Kafka listener started for topic '{self.topic}'.")

    def _listen_loop(self):
        """Continuously poll Kafka and send messages to the handler."""
        self.consumer.subscribe([self.topic])
        while True:
            msg = self.consumer.poll(0.25)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                self.logger.error(f"Consumer error: {msg.error()}")
                continue

            try:
                text = msg.value().decode("utf-8") if isinstance(msg.value(), bytes) else str(msg.value())
                self.logger.debug("got message from consumer: %s", text)

                if self.message_handler:
                    self.message_handler(text)

            except Exception as e:
                self.logger.error(f"Failed to process Kafka message: {e}")
