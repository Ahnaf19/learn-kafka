from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'host.docker.internal:9092'
}

p = Producer(**conf)

def delivery_report(err, msg):
    if err:
        print(f"❌ Message failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

p.produce('weather_data_demo', key='test', value='Hello Kafka', callback=delivery_report)
p.flush()
