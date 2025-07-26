import json
from pydoc_data import topics
from loguru import logger
from quixstreams import Application

def main():
    """
    Simple consumer that reads messages from the 'weather_data_demo' topic
    and prints them to the console.
    """
    app = Application(
        broker_address="host.docker.internal:9092",
        loglevel="DEBUG",
        # consumer group for 
        consumer_group="weather_reader"
    )

    """
    Use breakpoint() inside the while loop to debug. Useful pdb commands:
    - list: Show surrounding code
    - pp locals(): Pretty-print local variables
    - n: Next line
    - s: Step into function
    - c: Continue execution
    - q: Quit debugger
    """

    with app.get_consumer() as consumer:
        consumer.subscribe(["weather_data_demo"])
        
        while True:
            msg = consumer.poll(timeout=1)
            if msg is None:
                logger.info("No message received, waiting...")
            
            elif msg.error() is not None:
                raise Exception(f"Error while consuming message: {msg.error()}")
            
            else:
                raw_key = msg.key()
                if raw_key is not None and isinstance(raw_key, (bytes, bytearray)):
                    key = raw_key.decode("utf-8")
                else:
                    key = None

                raw_value = msg.value()
                if raw_value is not None and isinstance(raw_value, (bytes, bytearray)):
                    value = json.loads(raw_value.decode("utf-8"))
                else:
                    value = None
                
                offset = msg.offset()
                topic = msg.topic()

                logger.info(f"Received message with offset: {offset}, topic: {topic}, key: {key}, value: {value}")
                # logger.debug(f"Message details: {type(msg)}, key type: {type(key)}, value type: {type(value)}, offset type: {type(offset)}, topic type: {type(topic)}")
                # breakpoint()  # Pause here to debug when a message is received

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass          