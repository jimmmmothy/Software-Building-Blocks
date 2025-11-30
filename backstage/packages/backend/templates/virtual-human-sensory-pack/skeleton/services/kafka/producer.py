import json
from confluent_kafka import Producer
import logging


class KafkaProducer:
    def __init__(self, bootstrap_servers, request_topic):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.request_topic = request_topic
        self.logger = logging.getLogger(__name__)

    def kafka_delivery_report(self, err, msg):
        if err:
            self.logger.error(
                "Message delivery failed to Kafka topic:%s | error: %s",
                self.request_topic,
                err
            )
        else:
            self.logger.info(
                "Message delivered to Kafka topic:%s [partition:%s, offset:%s] | message: %s",
                msg.topic(),
                msg.partition(),
                msg.offset(),
                msg.value().decode('utf-8')  # decode the JSON string for readability
            )

    def send(self, user_message_dict):
        self.producer.produce(
            self.request_topic,
            json.dumps(user_message_dict).encode("utf-8"),
            callback=self.kafka_delivery_report
        )
        self.producer.flush()
