from loguru import logger
from quixstreams import Application
import json
from utils.kafka_message_handler import TopicAwareMessageHandler

def main():
    """Quick consumer to listen to weather_i18n topic and log messages"""
    
    app = Application(
        broker_address='host.docker.internal:9092',
        consumer_group='weather_listener',
        auto_offset_reset='earliest',  # Read from beginning to see all data
        loglevel='INFO'
    )
    
    # Subscribe to the weather_i18n topic
    topic = app.topic(name='weather_i18n', value_deserializer='json')
    
    # Initialize message handler with topic support
    message_handler = TopicAwareMessageHandler(topic=topic)
    
    logger.info("Starting weather_i18n consumer...")
    logger.info("Listening for messages on 'weather_i18n' topic...")
    logger.info("Press Ctrl+C to stop")
    
    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])
        
        message_count = 0
        
        while True:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                # No message received, continue listening
                continue
            
            # Process message using the handler
            processed_data = message_handler.process_message(msg)
            
            if processed_data:
                message_count += 1
                
                # Log the weather data in a nice format
                logger.info(f"Message #{message_count}")
                logger.info(f"Key: {processed_data['key']}")
                logger.info(f"Partition: {processed_data['partition']}, Offset: {processed_data['offset']}")
                logger.info(f"Weather Data: {json.dumps(processed_data['value'], indent=2)}")
                logger.info("-" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
    except Exception as e:
        logger.error(f"Consumer failed: {e}")
