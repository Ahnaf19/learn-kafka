from quixstreams import Application

app = Application(
    broker_address="docker.host.internal:9092",
    loglevel="DEBUG",
    # consumer group for 
    consumer_group="weather_reader"
)

"""
can use breakpoint() inside the while loop, to see what's going on use commands like:
 - list
 - pp locals()
"""

with app.get_consumer() as consumer:
    consumer.subscribe(["weather_data_demo"])
    
    while True:
        consumer.poll(timeout=1)
        # if msg is None:
        breakpoint()