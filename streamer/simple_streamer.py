from loguru import logger
from quixstreams import Application

from utils.temp_transform import i8n_weather

def main():
    app = Application(
        broker_address='host.docker.internal:9092',
        loglevel='DEBUG',
        auto_offset_reset='latest',
        consumer_group='weather_streamer',
    )
    
    input_topic = app.topic(
        name='weather_data_demo', value_serializer='json'
    )
    output_topic = app.topic(
        name='weather_i18n', value_serializer='json')

    sdf = app.dataframe(topic=input_topic) # Create a DataFrame from the input topic
    sdf = sdf.apply(i8n_weather) # Transform the temperature data
    sdf = sdf.to_topic(output_topic) # produces the sdf to the output topic
    
    app.run(sdf)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Keyboard interruption detected, streamer stopped")
    except Exception as e:
        logger.error(f"Streamer failed: {e}")