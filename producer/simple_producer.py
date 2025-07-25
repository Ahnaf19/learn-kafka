import json
import time
from quixstreams import Application
from loguru import logger

from weather_api.open_meteo_api import get_weather_data

app = Application(
    broker_address='host.docker.internal:9092',
    loglevel='DEBUG',
)

weather_topic = app.topic(
    name='weather_data_demo', value_serializer='json'
)

messages = [
    {"chat_id": "id1", "text": "Lorem ipsum dolor sit amet"},
    {"chat_id": "id2", "text": "Consectetur adipiscing elit sed"},
    {"chat_id": "id1", "text": "Do eiusmod tempor incididunt ut labore et"},
    {"chat_id": "id3", "text": "Mollis nunc sed id semper"},
]

"""
for testing purpose, use these messages inside a for loop and pass them to the topic as key-value pairs.

with app.get_producer() as producer:
        for message in messages:
            # Serialize message to send it to Kafka
            kafka_msg = weather_topic.serialize(key='dhaka-weather', value=message)
            producer.produce(topic=..., key=..., value=...)
"""

def main():
    with app.get_producer() as producer:
        while True:
            weather = get_weather_data()
            logger.debug(f'Got weather: {weather}\n')

            kafka_msg = weather_topic.serialize(key='dhaka-weather', value=json.dumps(weather))

            # Produce message to the topic
            logger.info(f'Produce event with key="{kafka_msg.key}" value="{kafka_msg.value}"')
            producer.produce(
                topic=weather_topic.name,
                key=kafka_msg.key,
                value=kafka_msg.value,
            )

            logger.info('Produced. Sleeping...')
            time.sleep(10)
        
        
if __name__ == "__main__":
    main()