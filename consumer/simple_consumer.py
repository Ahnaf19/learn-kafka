# consumer/simple_consumer.py

from loguru import logger
from quixstreams import Application

from utils.kafka_message_handler import TopicAwareMessageHandler


def main():
    """
    Simple consumer that reads messages from the 'weather_data_demo' topic
    and prints them to the console.
    """
    app = Application(
        broker_address="host.docker.internal:9092",
        loglevel="DEBUG",
        consumer_group="weather_reader", # allows multiple consumers to read from the same topic
        auto_offset_reset="latest", # Start reading from the "earliest" message. Default is "latest"
    )

    weather_topic = app.topic(name="weather_data_demo", value_serializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([weather_topic.name])
        
        while True:
            msg = consumer.poll(timeout=5) # Poll for new messages waiting up to 5 second

            handler = TopicAwareMessageHandler(topic=weather_topic)
            processed_data = handler.process_message(msg)
            if processed_data:
                handler.log_processed_message(processed_data)
                # storing offsets help to start from the next message on the next run
                consumer.store_offsets(msg) # Store the offset after processing the message

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Keyboard interruption detected, consumer stopped")
    except Exception as e:
        logger.error(f"Consumer failed: {e}")