# QuixStreams Kafka Client Guide

## Table of Contents

- [What is Apache Kafka?](#what-is-apache-kafka)
- [Kafka with Docker](#kafka-with-docker)
- [Python Kafka Clients Comparison](#python-kafka-clients-comparison)
- [QuixStreams Overview](#quixstreams-overview)
- [Application Configuration](#application-configuration)
- [Producer Setup](#producer-setup)
- [Consumer Setup](#consumer-setup)
- [Topic Management](#topic-management)
- [Message Processing](#message-processing)
- [Serialization Options](#serialization-options)
- [Offset Management](#offset-management)
- [Consumer Groups](#consumer-groups)
- [Logging Configuration](#logging-configuration)
- [Triggers and Timing](#triggers-and-timing)
- [Error Handling](#error-handling)
- [StreamingDataFrame (SDF) Processing](#streamingdataframe-sdf-processing)
- [Advanced Features](#advanced-features)

## What is Apache Kafka?

**Apache Kafka** is a distributed streaming platform designed for building real-time data pipelines and streaming applications.

### Core Concepts

#### 📖 **Topics** - Named Message Categories

A **topic** is a named category where related messages are stored, like a dedicated mailbox for specific types of data.

_Example: All user login events go to "user-logins" topic, all sensor readings go to "temperature-data" topic._

#### 📄 **Partitions** - Parallel Processing Lanes

A **partition** is a subdivision of a topic that allows parallel processing, like having multiple checkout lanes at a store.

_Example: A "user-events" topic with 3 partitions lets 3 consumers process user events simultaneously._

#### 🔢 **Offsets** - Message Position Numbers

An **offset** is the unique position number of each message within a partition, starting from 0 and incrementing sequentially.

_Example: Message at offset 42 in partition 2 is the 43rd message in that specific partition._

#### 📤 **Producers** - Message Senders

A **producer** is an application that sends messages to Kafka topics, choosing which topic to write to.

_Example: Your IoT sensor app acting as a producer, sending temperature readings to the "sensor-data" topic._

#### 📥 **Consumers** - Message Readers

A **consumer** is an application that reads messages from Kafka topics, keeping track of which messages it has already processed.

_Example: Your analytics service acting as a consumer, reading all temperature data to generate reports._

#### 🏢 **Brokers** - Kafka Server Instances

A **broker** is a Kafka server that stores and serves messages, with multiple brokers working together for reliability.

_Example: Running 3 brokers means if one server fails, the other 2 can continue serving your data._

#### 👥 **Consumer Groups** - Coordinated Processing Teams

A **consumer group** is a team of consumers that work together to process messages, automatically splitting the workload.

_Example: Having 3 consumers in the "analytics-team" group means they'll automatically divide partitions among themselves._

### Key Benefits (Why Use Kafka?)

- **🚀 High Throughput**: Handle millions of messages per second (like a massive automated sorting facility)
- **📈 Scalability**: Horizontally scalable across multiple machines (add more post offices)
- **💾 Durability**: Data is persisted to disk and replicated (backup copies in multiple locations)
- **🛡️ Fault Tolerance**: Automatic failover and recovery (if one post office fails, others take over)
- **⚡ Real-time Processing**: Low-latency message delivery (express mail service)

## Kafka with Docker

### Docker Compose Setup

Our project uses Docker Compose to run Kafka locally for development.

```yaml
version: "3.8"
services:
  kafka:
    image: apache/kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://host.docker.internal:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

### How It Works

1. **🏢 Single Broker**: Runs one Kafka broker for development

   - **Production**: You'd have multiple brokers for redundancy

2. **🚪 Port Mapping**: Exposes Kafka on port 9092

   - **Technical**: `localhost:9092` is how applications connect to Kafka

3. **🌐 Network Access**: Uses `host.docker.internal` for container-to-host communication

   - **Analogy**: Like a forwarding address that works between the container and your computer
   - **Why needed**: Docker containers need special addressing to talk to your local machine

4. **📦 Auto Topic Creation**: Automatically creates topics when first accessed
   - **Analogy**: Like automatically creating new mailbox sections when someone tries to send mail there
   - **Behavior**: First message to "my-topic" creates the topic automatically

### Docker Commands (Post Office Management)

```bash
# 🔧 Start Kafka (Open the post office)
docker-compose up -d

# 📋 Check logs (Check post office activity reports)
docker-compose logs kafka

# 🛑 Stop Kafka (Close the post office, keep the mailboxes)
docker-compose down

# 🗑️ Stop and delete all data (Demolish the post office and all mailboxes)
docker-compose down -v
```

### 🔍 Data Persistence Explained

**What happens when you restart?**

| Command                  | Data Preserved? | Analogy                                   |
| ------------------------ | --------------- | ----------------------------------------- |
| `docker-compose down`    | ✅ YES          | Close post office, mailboxes remain       |
| `docker-compose down -v` | ❌ NO           | Demolish everything, start fresh          |
| System restart           | ✅ YES          | Power outage, but building is still there |

**Why offsets persist**: Kafka stores everything in `/var/lib/kafka` inside the container, which is persisted as a Docker volume.

## Python Kafka Clients Comparison

| Feature               | kafka-python | confluent-kafka | QuixStreams |
| --------------------- | ------------ | --------------- | ----------- |
| **Performance**       | Moderate     | High            | High        |
| **Ease of Use**       | Complex      | Moderate        | Simple      |
| **Stream Processing** | None         | Basic           | Advanced    |
| **Schema Registry**   | Manual       | Built-in        | Built-in    |
| **Error Handling**    | Manual       | Good            | Excellent   |
| **Documentation**     | Good         | Excellent       | Good        |
| **Learning Curve**    | Steep        | Moderate        | Gentle      |

### Why Choose QuixStreams?

- **Simplified API**: Easier to learn and use
- **Built-in Stream Processing**: DataFrame-like operations
- **Automatic Error Handling**: Robust retry mechanisms
- **Modern Python**: Type hints and async support
- **Development Focus**: Great for rapid prototyping

## QuixStreams Overview

QuixStreams is a Python library that simplifies Kafka application development with a focus on stream processing. It provides both traditional producer/consumer APIs and a pandas-like DataFrame API for stream processing.

### Key Features

- Simple Application configuration
- Built-in serialization/deserialization
- DataFrame-style stream processing
- Automatic error handling and retries
- Consumer group management
- Schema registry integration
- Exactly-once processing guarantees

## Application Configuration

### Application Setup Options

| Option               | Description                           | Default Value | Example            | Use Case              |
| -------------------- | ------------------------------------- | ------------- | ------------------ | --------------------- |
| `broker_address`     | Kafka broker connection string        | Required      | `"localhost:9092"` | Basic connection      |
| `consumer_group`     | Consumer group identifier             | Required      | `"my-group"`       | Consumer coordination |
| `auto_offset_reset`  | Where to start reading when no offset | `"latest"`    | `"earliest"`       | Replay all messages   |
| `loglevel`           | Logging verbosity level               | `"INFO"`      | `"DEBUG"`          | Debugging issues      |
| `auto_commit_enable` | Automatic offset commits              | `True`        | `False`            | Manual offset control |
| `commit_interval`    | Auto-commit frequency (ms)            | `5000`        | `1000`             | Faster commits        |
| `request_timeout_ms` | Request timeout                       | `30000`       | `10000`            | Faster timeouts       |
| `security_protocol`  | Security protocol                     | `"PLAINTEXT"` | `"SASL_SSL"`       | Secure connections    |

### Basic Configuration

```python
from quixstreams import Application

# Standard local development
app = Application(
    broker_address="localhost:9092",
    consumer_group="my-group",
    auto_offset_reset="earliest",
    loglevel="INFO"
)
```

### Docker Environment Configuration

```python
# For Docker Compose setup
app = Application(
    broker_address="host.docker.internal:9092",
    consumer_group="docker-group",
    auto_offset_reset="latest"
)
```

### Production Configuration

```python
# Production with security and tuning
app = Application(
    broker_address="prod-broker:9092",
    consumer_group="prod-group",
    auto_offset_reset="earliest",
    loglevel="WARNING",
    request_timeout_ms=10000,
    auto_commit_enable=False,  # Manual offset management
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_username="username",
    sasl_password="password"
)
```

## Producer Setup

### Understanding Producers

Think of **Producers** as **people sending letters** through a sophisticated postal system. They decide what to send, where to send it, and how important it is.

#### 📤 **Producer Behavior Explained**

| Concept                  | Technical                          | Mail Analogy                               |
| ------------------------ | ---------------------------------- | ------------------------------------------ |
| **Topic Selection**      | Choose which topic to send to      | Choose which mailbox (address)             |
| **Partition Assignment** | Kafka assigns message to partition | Post office chooses which slot in mailbox  |
| **Key-based Routing**    | Same key → same partition          | Same recipient → same mail slot            |
| **Acknowledgments**      | Wait for confirmation              | Wait for delivery receipt                  |
| **Batching**             | Group messages for efficiency      | Collect multiple letters before postal run |

### Producer Configuration Options

| Option                   | Description                | Default Value | Example  | Mail Analogy                   |
| ------------------------ | -------------------------- | ------------- | -------- | ------------------------------ |
| `acks`                   | Acknowledgment level       | `1`           | `"all"`  | Delivery confirmation type     |
| `retries`                | Number of retry attempts   | `2147483647`  | `3`      | How many delivery attempts     |
| `batch_size`             | Batch size in bytes        | `16384`       | `32768`  | Letters per postal bag         |
| `linger_ms`              | Delay before sending batch | `0`           | `100`    | Wait time to fill bag          |
| `compression_type`       | Message compression        | `"none"`      | `"gzip"` | Compress letters to save space |
| `max_in_flight_requests` | Concurrent requests        | `5`           | `1`      | Postal trucks on the road      |
| `enable_idempotence`     | Exactly-once semantics     | `False`       | `True`   | Prevent duplicate deliveries   |

### 📮 **Acknowledgment Levels (Delivery Confirmation)**

```python
# 🚚 "acks=1" (Default) - Basic delivery confirmation
basic_producer = Application(
    broker_address="localhost:9092",
    acks=1  # Wait for leader broker confirmation only
)
# Analogy: "Mail delivered to local post office"

# 🏢 "acks=all" - Full delivery confirmation
reliable_producer = Application(
    broker_address="localhost:9092",
    acks="all"  # Wait for all replica brokers to confirm
)
# Analogy: "Mail delivered AND signed for by all postal centers"

# ⚡ "acks=0" - No delivery confirmation (fire and forget)
fast_producer = Application(
    broker_address="localhost:9092",
    acks=0  # Don't wait for any confirmation
)
# Analogy: "Drop mail in box and walk away"
```

### Basic Producer

```python
from quixstreams import Application

def simple_mail_sender():
    """Basic producer - like sending regular mail"""

    app = Application(broker_address="localhost:9092")

    # 📮 Choose your mailbox (topic)
    mailbox = app.topic(name="customer-notifications", value_serializer="json")

    # 📤 Send some letters (messages)
    with app.get_producer() as mail_sender:
        for customer_id in range(10):
            letter = {
                "customer_id": customer_id,
                "message": f"Thank you for your order, Customer {customer_id}!",
                "timestamp": time.time()
            }

            # 🏷️ Address the letter (serialize with key for routing)
            addressed_letter = mailbox.serialize(
                key=f"customer-{customer_id}",  # Customer address (routing key)
                value=letter  # Letter content
            )

            # 📬 Drop in mailbox
            mail_sender.produce(
                topic=mailbox.name,
                key=addressed_letter.key,
                value=addressed_letter.value
            )

            print(f"📮 Sent notification to customer-{customer_id}")

        # 🚚 Make sure all mail is sent before closing
        mail_sender.flush()
        print("✅ All notifications sent!")
```

### High-Throughput Producer (Bulk Mail Service)

```python
def bulk_mail_service():
    """High-throughput producer - like a bulk mail service"""

    app = Application(
        broker_address="localhost:9092",
        # 📦 Bulk mail optimizations
        acks="all",                    # Full delivery confirmation
        retries=3,                     # Try 3 times if delivery fails
        batch_size=32768,              # Bigger mail bags (32KB)
        linger_ms=100,                 # Wait 100ms to fill bags
        compression_type="gzip"        # Compress mail to save space
    )

    mailbox = app.topic(name="bulk-notifications", value_serializer="json")

    with app.get_producer() as bulk_sender:
        print("📦 Starting bulk mail service...")

        # 📬 Send thousands of letters efficiently
        letters = [
            {
                "id": i,
                "timestamp": time.time(),
                "campaign": "holiday-sale",
                "message": f"Special offer for customer {i}!"
            }
            for i in range(10000)
        ]

        for letter in letters:
            addressed_letter = mailbox.serialize(
                key=str(letter["id"]),
                value=letter
            )

            bulk_sender.produce(
                topic=mailbox.name,
                key=addressed_letter.key,
                value=addressed_letter.value
            )

            # 📊 Progress reporting
            if letter["id"] % 1000 == 0:
                print(f"📦 Processed {letter['id']} letters...")

        # 🚛 Ensure all mail trucks have left
        print("🚛 Sending all mail trucks...")
        bulk_sender.flush()
        print("✅ All 10,000 letters sent successfully!")
```

### Producer with Delivery Confirmation (Registered Mail)

```python
def registered_mail_service():
    """Producer with full delivery tracking - like registered mail"""

    app = Application(
        broker_address="localhost:9092",
        acks="all",                    # Wait for all postal centers to confirm
        enable_idempotence=True,       # Prevent duplicate deliveries
        retries=5                      # Try up to 5 times
    )

    important_mailbox = app.topic(name="critical-transactions", value_serializer="json")

    with app.get_producer() as registered_sender:
        critical_messages = [
            {"transaction_id": "TXN-001", "amount": 1000.00, "type": "payment"},
            {"transaction_id": "TXN-002", "amount": 250.50, "type": "refund"},
            {"transaction_id": "TXN-003", "amount": 75.25, "type": "payment"}
        ]

        for msg in critical_messages:
            try:
                print(f"📮 Sending critical transaction: {msg['transaction_id']}")

                # 🏷️ Address the registered mail
                registered_letter = important_mailbox.serialize(
                    key=msg["transaction_id"],
                    value=msg
                )

                # 📬 Send registered mail
                registered_sender.produce(
                    topic=important_mailbox.name,
                    key=registered_letter.key,
                    value=registered_letter.value
                )

                # 🚚 Wait for delivery confirmation
                registered_sender.flush(timeout=10.0)  # Wait up to 10 seconds
                print(f"✅ Transaction {msg['transaction_id']} delivered successfully!")

            except Exception as e:
                print(f"❌ Failed to deliver {msg['transaction_id']}: {e}")
                # In production, you might send to a dead letter queue
```

### Smart Routing with Keys (Address-based Delivery)

```python
def smart_routing_example():
    """Demonstrates how message keys affect partition assignment"""

    app = Application(broker_address="localhost:9092")

    # 🏘️ Neighborhood mailbox with multiple slots (partitions)
    neighborhood = app.topic(name="user-events", value_serializer="json")

    with app.get_producer() as mail_carrier:
        print("🏘️ Delivering mail to neighborhood with smart routing...")

        users = ["alice", "bob", "charlie", "alice", "bob", "diana"]

        for user in users:
            event = {
                "user": user,
                "action": "login",
                "timestamp": time.time()
            }

            # 🎯 Key insight: Same user → Same partition
            # This ensures all events for a user are in order
            letter = neighborhood.serialize(
                key=user,  # User name as routing key
                value=event
            )

            mail_carrier.produce(
                topic=neighborhood.name,
                key=letter.key,
                value=letter.value
            )

            print(f"📮 Delivered {user}'s event (always goes to same mailbox slot)")

        mail_carrier.flush()

        print("🎯 Key insight: All events for the same user go to the same partition")
        print("📊 This maintains chronological order per user")
```

### 🧭 **Choosing Producer Configuration**

| Use Case             | Configuration              | Analogy            | Trade-offs               |
| -------------------- | -------------------------- | ------------------ | ------------------------ |
| **High Speed**       | `acks=0`, no retries       | Drop mail and run  | Fast but risky           |
| **Balanced**         | `acks=1`, some retries     | Standard mail      | Good speed + reliability |
| **Critical Data**    | `acks=all`, idempotence    | Registered mail    | Slow but guaranteed      |
| **Bulk Processing**  | Large batches, compression | Bulk mail service  | Efficient for volume     |
| **Ordered Messages** | `max_in_flight_requests=1` | One delivery truck | Maintains order          |

## Consumer Setup

### Consumer Configuration Options

| Option                    | Description              | Default Value | Example | Use Case           |
| ------------------------- | ------------------------ | ------------- | ------- | ------------------ |
| `enable_auto_commit`      | Automatic offset commits | `True`        | `False` | Manual control     |
| `auto_commit_interval_ms` | Auto-commit frequency    | `5000`        | `1000`  | Faster commits     |
| `max_poll_records`        | Records per poll() call  | `500`         | `100`   | Smaller batches    |
| `max_poll_interval_ms`    | Max time between polls   | `300000`      | `30000` | Faster rebalancing |
| `session_timeout_ms`      | Session timeout          | `10000`       | `30000` | Network tolerance  |
| `heartbeat_interval_ms`   | Heartbeat frequency      | `3000`        | `1000`  | Faster detection   |
| `fetch_min_bytes`         | Minimum fetch size       | `1`           | `1024`  | Reduce round trips |
| `fetch_max_wait_ms`       | Max wait for fetch       | `500`         | `100`   | Lower latency      |

### Basic Consumer

```python
from quixstreams import Application

app = Application(
    broker_address="localhost:9092",
    consumer_group="my-consumer-group"
)

topic = app.topic(name="my-topic", value_deserializer="json")

with app.get_consumer() as consumer:
    consumer.subscribe([topic.name])

    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        # Process message
        print(f"Key: {msg.key()}, Value: {msg.value()}")
```

### Consumer with Manual Offset Management

```python
def manual_offset_consumer():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="manual-group",
        enable_auto_commit=False,      # Disable auto-commit
        max_poll_records=10           # Process smaller batches
    )

    topic = app.topic(name="my-topic", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                continue

            try:
                # Process message
                process_message(msg.value())

                # Manually commit offset after successful processing
                consumer.commit(msg)
                print(f"Processed and committed offset {msg.offset()}")

            except Exception as e:
                print(f"Failed to process message: {e}")
                # Don't commit on error - message will be reprocessed
```

### High-Performance Consumer

```python
def high_performance_consumer():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="high-perf-group",
        max_poll_records=1000,         # Larger batches
        fetch_min_bytes=8192,          # Reduce round trips
        fetch_max_wait_ms=100,         # Lower latency
        session_timeout_ms=30000       # More tolerance
    )

    topic = app.topic(name="high-volume", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                continue

            # Process with topic deserialization
            try:
                deserialized_msg = topic.deserialize(msg)
                value = deserialized_msg.value

                # Batch processing logic here
                process_batch([value])

            except Exception as e:
                print(f"Processing error: {e}")
```

## Topic Management

### Topic Configuration Options

| Option               | Description                  | Default Value | Example      | Use Case            |
| -------------------- | ---------------------------- | ------------- | ------------ | ------------------- |
| `name`               | Topic name                   | Required      | `"my-topic"` | Topic identifier    |
| `value_serializer`   | Value serialization format   | `None`        | `"json"`     | Data format control |
| `key_serializer`     | Key serialization format     | `None`        | `"str"`      | Key format control  |
| `value_deserializer` | Value deserialization format | `None`        | `"json"`     | Data parsing        |
| `key_deserializer`   | Key deserialization format   | `None`        | `"str"`      | Key parsing         |
| `num_partitions`     | Number of partitions         | `1`           | `3`          | Parallelism         |
| `replication_factor` | Replication factor           | `1`           | `3`          | Fault tolerance     |

### Topic Creation and Configuration

```python
from quixstreams import Application

app = Application(broker_address="localhost:9092")

# JSON topic (most common)
json_topic = app.topic(
    name="json-data",
    value_serializer="json",
    key_serializer="str"
)

# String topic
string_topic = app.topic(
    name="text-data",
    value_serializer="str",
    key_serializer="str"
)

# Bytes topic (raw data)
bytes_topic = app.topic(
    name="binary-data",
    value_serializer="bytes",
    key_serializer="bytes"
)

# Integer values with string keys
int_topic = app.topic(
    name="metrics",
    value_serializer="int",
    key_serializer="str"
)
```

### Producer vs Consumer Topic Setup

```python
# Producer topic (use serializers)
producer_topic = app.topic(
    name="weather-data",
    value_serializer="json",
    key_serializer="str"
)

# Consumer topic (use deserializers)
consumer_topic = app.topic(
    name="weather-data",
    value_deserializer="json",
    key_deserializer="str"
)

# Example usage
with app.get_producer() as producer:
    data = {"temperature": 25.5, "humidity": 60}
    kafka_msg = producer_topic.serialize(key="sensor-1", value=data)
    producer.produce(
        topic=producer_topic.name,
        key=kafka_msg.key,
        value=kafka_msg.value
    )

with app.get_consumer() as consumer:
    consumer.subscribe([consumer_topic.name])
    msg = consumer.poll(timeout=1.0)
    if msg and not msg.error():
        deserialized = consumer_topic.deserialize(msg)
        print(f"Received: {deserialized.value}")
```

## Message Processing

### Message Structure and Properties

| Property          | Description       | Type         | Example              | Use Case       |
| ----------------- | ----------------- | ------------ | -------------------- | -------------- |
| `msg.key()`       | Message key       | `bytes`      | `b"user-123"`        | Partitioning   |
| `msg.value()`     | Message value     | `bytes`      | `b'{"temp":25}'`     | Actual data    |
| `msg.topic()`     | Topic name        | `str`        | `"sensor-data"`      | Routing        |
| `msg.partition()` | Partition number  | `int`        | `2`                  | Debugging      |
| `msg.offset()`    | Message offset    | `int`        | `12345`              | Tracking       |
| `msg.timestamp()` | Message timestamp | `tuple`      | `(1, 1642678800000)` | Event time     |
| `msg.error()`     | Error information | `KafkaError` | `None`               | Error handling |

### Complete Message Processing Pipeline

```python
import json
from loguru import logger

def process_kafka_message(msg, topic):
    """Complete message processing workflow with error handling"""

    # 1. Validate message
    if msg is None:
        logger.warning("Received None message")
        return None

    if msg.error():
        logger.error(f"Message error: {msg.error()}")
        return None

    # 2. Extract metadata
    metadata = {
        "offset": msg.offset(),
        "partition": msg.partition(),
        "topic": msg.topic(),
        "timestamp": msg.timestamp()[1] if msg.timestamp()[0] else None
    }

    # 3. Decode key
    try:
        key = msg.key().decode('utf-8') if msg.key() else None
    except UnicodeDecodeError:
        logger.warning(f"Failed to decode key: {msg.key()}")
        key = str(msg.key())

    # 4. Deserialize value
    try:
        # Try QuixStreams deserialization first
        deserialized_msg = topic.deserialize(msg)
        value = deserialized_msg.value
        logger.debug(f"Deserialized using QuixStreams: {type(value)}")

    except Exception as e:
        logger.warning(f"QuixStreams deserialization failed: {e}")
        try:
            # Fallback to manual JSON deserialization
            raw_value = msg.value().decode('utf-8')
            value = json.loads(raw_value)
            logger.debug("Fallback to manual JSON deserialization")

        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logger.error(f"All deserialization attempts failed: {e}")
            value = msg.value()  # Return raw bytes

    return {
        "key": key,
        "value": value,
        "metadata": metadata,
        "raw_message": msg
    }
```

### Message Validation and Filtering

```python
def validate_and_filter_message(processed_msg):
    """Validate message content and apply business logic filters"""

    if processed_msg is None:
        return False

    value = processed_msg["value"]

    # Basic validation
    if not isinstance(value, dict):
        logger.warning(f"Expected dict, got {type(value)}")
        return False

    # Required fields validation
    required_fields = ["timestamp", "sensor_id", "reading"]
    if not all(field in value for field in required_fields):
        logger.warning(f"Missing required fields: {required_fields}")
        return False

    # Business logic filters
    if value.get("reading", 0) < 0:
        logger.info("Filtering out negative readings")
        return False

    return True
```

## Serialization Options

### Built-in Serializers

| Serializer | Description            | Input Type     | Output Type | Example            |
| ---------- | ---------------------- | -------------- | ----------- | ------------------ |
| `"json"`   | JSON serialization     | `dict`, `list` | `bytes`     | `{"key": "value"}` |
| `"str"`    | String serialization   | `str`          | `bytes`     | `"hello world"`    |
| `"bytes"`  | Raw bytes              | `bytes`        | `bytes`     | `b"raw data"`      |
| `"int"`    | Integer serialization  | `int`          | `bytes`     | `42`               |
| `"double"` | Double precision float | `float`        | `bytes`     | `3.14159`          |

### Serialization Examples

```python
from quixstreams import Application

app = Application(broker_address="localhost:9092")

# JSON serialization (most common for structured data)
json_topic = app.topic(
    name="weather-data",
    value_serializer="json",
    key_serializer="str"
)

# Usage with producer
with app.get_producer() as producer:
    weather_data = {
        "temperature": 25.5,
        "humidity": 60,
        "location": "NYC",
        "timestamp": "2024-01-01T12:00:00Z"
    }

    kafka_msg = json_topic.serialize(
        key="sensor-001",
        value=weather_data
    )

    producer.produce(
        topic=json_topic.name,
        key=kafka_msg.key,
        value=kafka_msg.value
    )

# String serialization (for log messages)
log_topic = app.topic(
    name="application-logs",
    value_serializer="str",
    key_serializer="str"
)

with app.get_producer() as producer:
    log_message = "INFO: Application started successfully"
    kafka_msg = log_topic.serialize(key="app-server-1", value=log_message)
    producer.produce(
        topic=log_topic.name,
        key=kafka_msg.key,
        value=kafka_msg.value
    )

# Bytes serialization (for binary data)
binary_topic = app.topic(
    name="file-data",
    value_serializer="bytes",
    key_serializer="str"
)

with app.get_producer() as producer:
    with open("data.bin", "rb") as f:
        binary_data = f.read()

    kafka_msg = binary_topic.serialize(key="file-123", value=binary_data)
    producer.produce(
        topic=binary_topic.name,
        key=kafka_msg.key,
        value=kafka_msg.value
    )
```

### Custom Serialization

```python
import pickle
import json
from datetime import datetime

class CustomSerializer:
    """Custom serializer for complex Python objects"""

    @staticmethod
    def serialize_datetime(obj):
        """Serialize datetime objects to JSON"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    @staticmethod
    def deserialize_datetime(json_str):
        """Deserialize JSON string with datetime objects"""
        def parse_datetime(dct):
            for key, value in dct.items():
                if isinstance(value, str) and value.endswith('Z'):
                    try:
                        dct[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        pass
            return dct

        return json.loads(json_str, object_hook=parse_datetime)

# Using custom serialization
def custom_producer():
    app = Application(broker_address="localhost:9092")

    # Raw topic without built-in serialization
    topic = app.topic(name="custom-data")

    with app.get_producer() as producer:
        data = {
            "event_time": datetime.now(),
            "user_id": 12345,
            "action": "login"
        }

        # Custom serialization
        serialized_data = json.dumps(
            data,
            default=CustomSerializer.serialize_datetime
        ).encode('utf-8')

        producer.produce(
            topic=topic.name,
            key=b"user-12345",
            value=serialized_data
        )
```

## Offset Management

### Understanding Offsets (Bookmark Analogy)

Think of **offsets** as **bookmarks in different books** (partitions). Each consumer group maintains its own set of bookmarks.

#### 🔢 **Offset Behavior Explained**

| Scenario                | What Happens                        | Bookmark Analogy                       |
| ----------------------- | ----------------------------------- | -------------------------------------- |
| New consumer group      | Starts based on `auto_offset_reset` | New reader choosing where to start     |
| Existing consumer group | Resumes from last committed offset  | Continues from bookmarked page         |
| Topic recreation        | Offsets reset to 0                  | New book, start from page 1            |
| Partition count change  | New topic created                   | Different book with different chapters |

### Offset Management Options

| Option                    | Description                         | Default Value | Example      | Bookmark Analogy        |
| ------------------------- | ----------------------------------- | ------------- | ------------ | ----------------------- |
| `auto_offset_reset`       | Starting position for new consumers | `"latest"`    | `"earliest"` | Where new readers start |
| `enable_auto_commit`      | Automatic offset commits            | `True`        | `False`      | Auto-bookmark vs manual |
| `auto_commit_interval_ms` | Auto-commit frequency               | `5000`        | `1000`       | How often to bookmark   |

### 🧪 **`auto_offset_reset` Behavior Explained**

**When does this setting matter?** Only when your consumer group has **no previous offset** (like a first-time magazine subscriber).

```python
# 📖 "earliest" = "Send me all back issues"
earliest_app = Application(
    broker_address="localhost:9092",
    consumer_group="archive-readers",
    auto_offset_reset="earliest"  # Start from the very beginning
)

# 📰 "latest" = "Send me only new issues"
latest_app = Application(
    broker_address="localhost:9092",
    consumer_group="real-time-readers",
    auto_offset_reset="latest"  # Skip existing messages, wait for new ones
)
```

**Common Confusion**: "Why do I see offset=0 with 'latest'?"

- **Answer**: If it's a new topic with no messages when you start, "latest" position IS 0
- **Analogy**: You subscribed to a magazine that hasn't published its first issue yet

### Automatic Offset Management (Auto-Bookmark)

```python
def auto_offset_consumer():
    """Consumer with automatic offset management (like auto-bookmarking)"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="auto-bookmark-group",
        auto_offset_reset="earliest",    # Start from beginning for new groups
        enable_auto_commit=True,         # Enable auto-bookmarking (default)
        auto_commit_interval_ms=5000     # Bookmark every 5 seconds
    )

    topic = app.topic(name="my-topic", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                continue

            # Process message
            print(f"📖 Reading page {msg.offset()} from chapter {msg.partition()}")
            process_message(msg.value())

            # 🔖 Bookmark will be updated automatically every 5 seconds
            # If your app crashes, you'll resume from the last auto-bookmark
```

### Manual Offset Management (Manual Bookmarking)

```python
def manual_offset_consumer():
    """Consumer with manual offset management (manual bookmarking for critical reading)"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="manual-bookmark-group",
        enable_auto_commit=False,        # Disable auto-bookmarking
        auto_offset_reset="earliest"
    )

    topic = app.topic(name="critical-data", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue

            try:
                # 📖 Process the message (read the page)
                result = process_critical_message(msg.value())

                if result.success:
                    # 🔖 Only bookmark after successful processing
                    consumer.commit(msg)
                    logger.info(f"✅ Bookmarked page {msg.offset()} after successful processing")
                else:
                    logger.warning(f"❌ Processing failed, NOT bookmarking page {msg.offset()}")
                    # Next restart will reprocess this message

            except Exception as e:
                logger.error(f"💥 Processing error: {e}")
                # Don't bookmark - message will be reprocessed after restart
```

### 🔄 **Offset Reset Strategies in Practice**

```python
# 🗄️ Data Replay Scenario (Read all history)
replay_app = Application(
    broker_address="localhost:9092",
    consumer_group="data-migration-team",  # New group name
    auto_offset_reset="earliest"  # Read everything from the beginning
)

# ⚡ Real-time Only Scenario (Skip history)
realtime_app = Application(
    broker_address="localhost:9092",
    consumer_group="alert-system",  # Different group name
    auto_offset_reset="latest"  # Only new messages matter
)

# 🎯 Custom Offset Management (Jump to specific page)
def seek_to_specific_offset():
    """Jump to a specific page number (offset) in the book (partition)"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="custom-position-group"
    )

    topic = app.topic(name="my-topic", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        # Wait for partition assignment (like getting your book)
        while not consumer.assignment():
            consumer.poll(timeout=0.1)

        # 🎯 Jump to page 1000 in all chapters (partitions)
        from confluent_kafka import TopicPartition
        partitions = [TopicPartition(topic.name, partition.partition, 1000)
                     for partition in consumer.assignment()]
        consumer.seek_to_offsets(partitions)

        logger.info("📖 Jumped to page 1000 in all chapters, starting to read...")

        # Now read from offset 1000 onwards
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg and not msg.error():
                print(f"Reading page {msg.offset()} from chapter {msg.partition()}")
                process_message(msg.value())
```

### 🧭 **Choosing the Right Offset Strategy**

| Use Case                | Strategy               | Analogy                          | Example                 |
| ----------------------- | ---------------------- | -------------------------------- | ----------------------- |
| **Data Migration**      | `earliest` + new group | Read entire encyclopedia         | Migrating all user data |
| **Real-time Alerts**    | `latest`               | Only today's newspaper           | System monitoring       |
| **Crash Recovery**      | Manual commits         | Careful bookmarking              | Financial transactions  |
| **Development/Testing** | `earliest`             | Read from beginning              | Understanding data flow |
| **Load Balancing**      | Same group             | Multiple readers, same bookmarks | Scaling consumer apps   |

````

## Consumer Groups

### Consumer Groups (Team Management Analogy)

Think of **Consumer Groups** as **work teams** where each team member handles different tasks, but all teams can work on the same project independently.

#### 👥 **How Consumer Groups Work**

| Concept | Technical | Team Analogy |
|---------|-----------|--------------|
| **Consumer Group** | Group of consumers with same group ID | A work team (e.g., "Data Processing Team") |
| **Partition Assignment** | Each consumer gets specific partitions | Each team member gets specific tasks/files |
| **Load Balancing** | Work is distributed automatically | Manager assigns tasks to available workers |
| **Fault Tolerance** | If consumer fails, others take over | If team member is sick, others cover their work |
| **Independent Teams** | Different groups process same data | Multiple teams can work on same project independently |

### Consumer Group Configuration

| Option                          | Description         | Default Value | Example              | Team Analogy           |
| ------------------------------- | ------------------- | ------------- | -------------------- | ---------------------- |
| `consumer_group`                | Consumer group ID   | Required      | `"processing-team"`  | Team name badge        |
| `session_timeout_ms`            | Session timeout     | `10000`       | `30000`              | "Check-in" frequency   |
| `heartbeat_interval_ms`         | Heartbeat frequency | `3000`        | `1000`               | "I'm alive" signals    |
| `max_poll_interval_ms`          | Max processing time | `300000`      | `60000`              | Max time per task      |
| `partition_assignment_strategy` | Assignment strategy | `"range"`     | `"roundrobin"`       | How to divide work     |

### Single Consumer Group (Team Load Balancing)

```python
def team_load_balancing_example():
    """Multiple workers in the same team sharing the workload"""

    # 👷‍♂️ Worker 1 (Team Member 1)
    app1 = Application(
        broker_address="localhost:9092",
        consumer_group="data-processing-team",  # Same team name
        session_timeout_ms=30000
    )

    # 👷‍♀️ Worker 2 (Team Member 2)
    app2 = Application(
        broker_address="localhost:9092",
        consumer_group="data-processing-team",  # Same team name
        session_timeout_ms=30000
    )

    topic = app1.topic(name="work-queue", value_deserializer="json")

    # 🎯 Key Behavior: Partitions are automatically split between team members
    # If topic has 4 partitions:
    # - Worker 1 might get partitions 0, 1
    # - Worker 2 might get partitions 2, 3
    # Each message is processed by exactly ONE team member

    with app1.get_consumer() as worker1, app2.get_consumer() as worker2:
        worker1.subscribe([topic.name])
        worker2.subscribe([topic.name])

        print("🏗️ Team started - work will be automatically distributed")
        print("📊 Each worker handles different partitions")
        print("⚖️ Load balancing happens automatically")

        # Both workers run simultaneously, handling different partitions
````

### Multiple Consumer Groups (Independent Teams)

```python
def independent_teams_example():
    """Different teams working on the same data independently"""

    # 🔄 Real-time Processing Team (for immediate alerts)
    realtime_team = Application(
        broker_address="localhost:9092",
        consumer_group="realtime-alerts-team",
        auto_offset_reset="latest"  # Only care about new events
    )

    # 📊 Analytics Team (for historical analysis)
    analytics_team = Application(
        broker_address="localhost:9092",
        consumer_group="analytics-research-team",
        auto_offset_reset="earliest"  # Need all historical data
    )

    # 🏪 Business Intelligence Team (for reports)
    bi_team = Application(
        broker_address="localhost:9092",
        consumer_group="business-intelligence-team",
        auto_offset_reset="earliest"  # All data for comprehensive reports
    )

    topic_name = "customer-events"

    # 🎯 Key Behavior: ALL teams receive ALL messages independently
    # - Realtime team gets every event (for immediate processing)
    # - Analytics team gets every event (for research)
    # - BI team gets every event (for reports)
    # Each team maintains its own progress (offsets)

    print("🏢 Multiple independent teams processing same data:")
    print("   📱 Realtime Team: Sends immediate notifications")
    print("   📈 Analytics Team: Updates dashboards and models")
    print("   📋 BI Team: Generates daily/weekly reports")
    print("   ✅ All teams see the same events but process them differently")
```

### Consumer Group Fault Tolerance (Team Resilience)

```python
def fault_tolerant_team_example():
    """Demonstrates how teams handle member failures"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="resilient-team",
        session_timeout_ms=10000,        # 10 seconds to detect failures
        heartbeat_interval_ms=3000,      # Heartbeat every 3 seconds
        max_poll_interval_ms=60000       # Max 60 seconds per task
    )

    topic = app.topic(name="critical-tasks", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        print("👷‍♂️ Team member started and ready for work")
        print("💓 Sending heartbeats to team coordinator every 3 seconds")
        print("⏰ Will be considered 'missing' if no heartbeat for 10 seconds")

        while True:
            try:
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    print("⏳ No work available, staying ready...")
                    continue

                if msg.error():
                    logger.error(f"❌ Work assignment error: {msg.error()}")
                    continue

                # 🎯 Simulate work processing
                print(f"🔨 Processing task {msg.offset()} from partition {msg.partition()}")

                # Simulate processing time
                import time
                time.sleep(2)  # 2 seconds of "work"

                print(f"✅ Completed task {msg.offset()}")

                # 📝 Report completion (commit offset)
                consumer.commit(msg)

            except KeyboardInterrupt:
                print("👋 Team member leaving gracefully")
                break
            except Exception as e:
                logger.error(f"💥 Team member encountered error: {e}")
                # Other team members will automatically take over this work
```

### Consumer Group Monitoring (Team Performance)

````python
def monitor_team_performance():
    """Monitor how well the team is performing"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="monitored-performance-team"
    )

    topic = app.topic(name="high-volume-tasks", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        # 📊 Performance tracking
        tasks_completed = 0
        start_time = time.time()
        last_report_time = start_time

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                # 📈 Report team performance every 30 seconds
                current_time = time.time()
                if current_time - last_report_time > 30:
                    elapsed = current_time - start_time
                    rate = tasks_completed / elapsed if elapsed > 0 else 0

                    print(f"📊 Team Performance Report:")
                    print(f"   ✅ Tasks completed: {tasks_completed}")
                    print(f"   ⏱️ Time elapsed: {elapsed:.1f} seconds")
                    print(f"   🚀 Processing rate: {rate:.2f} tasks/second")

                    last_report_time = current_time
                continue

            if msg.error():
                logger.error(f"❌ Team coordination error: {msg.error()}")
                continue

            # 🎯 Process the task
            try:
                process_message(msg.value())
                tasks_completed += 1

                # 📝 Log individual task completion
                if tasks_completed % 100 == 0:
                    print(f"🎯 Milestone: {tasks_completed} tasks completed")
                    print(f"   📍 Current position: offset {msg.offset()}, partition {msg.partition()}")

            except Exception as e:
                logger.error(f"💥 Task processing failed: {e}")

### 🧭 **Choosing Consumer Group Strategy**

| Scenario | Strategy | Analogy | Example |
|----------|----------|---------|---------|
| **Scale Processing** | Same group, multiple consumers | Bigger team, same project | Handle high message volume |
| **Different Use Cases** | Different groups | Different teams, same data | Alerts + Analytics + Reports |
| **Fault Tolerance** | Multiple consumers per group | Team with backup members | Critical message processing |
| **Development** | Unique group per developer | Each developer has own workspace | Isolated testing |

## Logging Configuration

### Logging Options

| Option         | Description            | Default Value | Example        | Use Case              |
| -------------- | ---------------------- | ------------- | -------------- | --------------------- |
| `loglevel`     | Application log level  | `"INFO"`      | `"DEBUG"`      | Detailed debugging    |
| Custom loggers | External logging setup | None          | Loguru/logging | Production monitoring |

### Built-in Logging

```python
from quixstreams import Application

# Debug level logging
debug_app = Application(
    broker_address="localhost:9092",
    consumer_group="debug-group",
    loglevel="DEBUG"  # Shows detailed QuixStreams internals
)

# Production logging (minimal)
prod_app = Application(
    broker_address="localhost:9092",
    consumer_group="prod-group",
    loglevel="WARNING"  # Only warnings and errors
)
````

### Loguru Integration

```python
from loguru import logger
from quixstreams import Application
import sys

# Configure Loguru
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Add file logging
logger.add(
    "kafka_app.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

def logged_consumer():
    """Consumer with comprehensive logging"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="logged-group",
        loglevel="INFO"  # QuixStreams logging
    )

    topic = app.topic(name="events", value_deserializer="json")

    logger.info("Starting consumer application")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])
        logger.info(f"Subscribed to topic: {topic.name}")

        while True:
            try:
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    logger.debug("No message received in poll timeout")
                    continue

                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

                # Log message details
                logger.info(f"Received message: offset={msg.offset()}, "
                           f"partition={msg.partition()}, key={msg.key()}")

                # Process with error logging
                try:
                    result = process_message(msg.value())
                    logger.success(f"Successfully processed message: {result}")

                except Exception as e:
                    logger.error(f"Processing failed: {e}")
                    logger.exception("Full error traceback:")

            except KeyboardInterrupt:
                logger.info("Consumer interrupted by user")
                break
            except Exception as e:
                logger.critical(f"Unexpected error: {e}")
                logger.exception("Critical error traceback:")
                break

    logger.info("Consumer application stopped")
```

### Structured Logging

```python
import json
from loguru import logger

def structured_logging_setup():
    """Setup structured JSON logging for production"""

    def json_formatter(record):
        """Custom JSON formatter for structured logs"""
        log_entry = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "logger": record["name"],
            "message": record["message"],
            "function": record["function"],
            "line": record["line"]
        }

        # Add extra fields if present
        if "extra" in record:
            log_entry.update(record["extra"])

        return json.dumps(log_entry)

    logger.add(
        "structured_kafka.log",
        format=json_formatter,
        level="INFO"
    )

def producer_with_structured_logging():
    """Producer with structured logging"""

    structured_logging_setup()

    app = Application(broker_address="localhost:9092")
    topic = app.topic(name="logged-events", value_serializer="json")

    with app.get_producer() as producer:
        for i in range(100):
            message = {"id": i, "data": f"message-{i}"}

            # Log with structured data
            logger.info(
                "Producing message",
                extra={
                    "message_id": i,
                    "topic": topic.name,
                    "message_size": len(str(message))
                }
            )

            try:
                kafka_msg = topic.serialize(key=f"key-{i}", value=message)
                producer.produce(
                    topic=topic.name,
                    key=kafka_msg.key,
                    value=kafka_msg.value
                )

                logger.debug(
                    "Message produced successfully",
                    extra={"message_id": i, "status": "success"}
                )

            except Exception as e:
                logger.error(
                    "Failed to produce message",
                    extra={
                        "message_id": i,
                        "error": str(e),
                        "status": "failed"
                    }
                )
```

## Triggers and Timing

### Timing Options

| Option               | Description            | Default Value | Example     | Use Case         |
| -------------------- | ---------------------- | ------------- | ----------- | ---------------- |
| `poll_timeout`       | Consumer poll timeout  | `1.0`         | `0.1`       | Low latency      |
| `flush_timeout`      | Producer flush timeout | `10.0`        | `5.0`       | Faster sends     |
| Processing intervals | Custom timing logic    | None          | Timer-based | Batch processing |

### Low-Latency Consumer

```python
import time
from quixstreams import Application

def low_latency_consumer():
    """Consumer optimized for low latency processing"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="low-latency-group",
        fetch_max_wait_ms=1,        # Minimal fetch wait
        heartbeat_interval_ms=1000  # Frequent heartbeats
    )

    topic = app.topic(name="realtime-events", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        while True:
            # Very short poll timeout for immediate processing
            msg = consumer.poll(timeout=0.01)  # 10ms timeout

            if msg is None:
                continue
            if msg.error():
                continue

            # Process immediately
            start_time = time.time()
            process_message(msg.value())
            processing_time = time.time() - start_time

            logger.debug(f"Processing time: {processing_time*1000:.2f}ms")
```

### Batch Processing with Timing

```python
import time
from collections import deque

def batch_consumer_with_timing():
    """Consumer that processes messages in timed batches"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="batch-group",
        max_poll_records=1000  # Large poll batches
    )

    topic = app.topic(name="batch-events", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        batch = deque()
        batch_start_time = time.time()
        batch_timeout = 10.0  # 10 seconds
        max_batch_size = 100

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg and not msg.error():
                batch.append(msg.value())

            # Process batch on timeout or size limit
            current_time = time.time()
            batch_age = current_time - batch_start_time

            if (len(batch) >= max_batch_size or
                (batch and batch_age >= batch_timeout)):

                logger.info(f"Processing batch of {len(batch)} messages "
                           f"(age: {batch_age:.1f}s)")

                # Process entire batch
                process_batch(list(batch))

                # Reset batch
                batch.clear()
                batch_start_time = current_time
```

### Scheduled Processing

```python
import threading
import time
from datetime import datetime, timedelta

def scheduled_producer():
    """Producer that sends messages on a schedule"""

    app = Application(broker_address="localhost:9092")
    topic = app.topic(name="scheduled-events", value_serializer="json")

    def send_periodic_message():
        """Send a message every 30 seconds"""
        with app.get_producer() as producer:
            while True:
                message = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "heartbeat",
                    "source": "scheduled-producer"
                }

                kafka_msg = topic.serialize(key="heartbeat", value=message)
                producer.produce(
                    topic=topic.name,
                    key=kafka_msg.key,
                    value=kafka_msg.value
                )
                producer.flush()

                logger.info(f"Sent scheduled message: {message}")
                time.sleep(30)  # Wait 30 seconds

    # Start in background thread
    thread = threading.Thread(target=send_periodic_message, daemon=True)
    thread.start()

    return thread

def time_window_consumer():
    """Consumer that processes messages in time windows"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="window-group"
    )

    topic = app.topic(name="windowed-events", value_deserializer="json")

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        window_start = datetime.now()
        window_duration = timedelta(minutes=5)  # 5-minute windows
        window_messages = []

        while True:
            msg = consumer.poll(timeout=1.0)
            current_time = datetime.now()

            if msg and not msg.error():
                window_messages.append({
                    "message": msg.value(),
                    "timestamp": current_time
                })

            # Check if window is complete
            if current_time - window_start >= window_duration:
                logger.info(f"Processing window with {len(window_messages)} messages")

                # Process entire window
                process_time_window(window_messages, window_start, current_time)

                # Start new window
                window_messages.clear()
                window_start = current_time
```

## Error Handling

### Error Handling Strategies

| Strategy                 | Description                            | Use Case           | Example                   |
| ------------------------ | -------------------------------------- | ------------------ | ------------------------- |
| **Retry**                | Retry failed operations                | Transient errors   | Network timeouts          |
| **Dead Letter Queue**    | Send failed messages to separate topic | Permanent failures | Malformed data            |
| **Circuit Breaker**      | Stop processing on repeated failures   | System protection  | Downstream service down   |
| **Graceful Degradation** | Continue with reduced functionality    | Partial failures   | Optional enrichment fails |

### Producer Error Handling

```python
import time
from quixstreams import Application
from loguru import logger

def robust_producer_with_retry():
    """Producer with comprehensive error handling and retry logic"""

    app = Application(
        broker_address="localhost:9092",
        acks="all",          # Wait for all replicas
        retries=3,           # Built-in retries
        enable_idempotence=True  # Prevent duplicates
    )

    topic = app.topic(name="reliable-events", value_serializer="json")
    dead_letter_topic = app.topic(name="failed-events", value_serializer="json")

    def send_message_with_retry(message, max_retries=3):
        """Send message with custom retry logic"""

        for attempt in range(max_retries + 1):
            try:
                with app.get_producer() as producer:
                    kafka_msg = topic.serialize(
                        key=message.get("id", "unknown"),
                        value=message
                    )

                    producer.produce(
                        topic=topic.name,
                        key=kafka_msg.key,
                        value=kafka_msg.value
                    )
                    producer.flush(timeout=5.0)  # 5 second timeout

                    logger.success(f"Message sent successfully: {message['id']}")
                    return True

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")

                if attempt < max_retries:
                    sleep_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"All retry attempts failed for message: {message}")

                    # Send to dead letter queue
                    try:
                        failed_message = {
                            "original_message": message,
                            "error": str(e),
                            "failed_at": time.time(),
                            "attempts": max_retries + 1
                        }

                        with app.get_producer() as dlq_producer:
                            dlq_msg = dead_letter_topic.serialize(
                                key=f"failed-{message.get('id')}",
                                value=failed_message
                            )
                            dlq_producer.produce(
                                topic=dead_letter_topic.name,
                                key=dlq_msg.key,
                                value=dlq_msg.value
                            )
                            dlq_producer.flush()

                        logger.info(f"Message sent to dead letter queue: {message['id']}")

                    except Exception as dlq_error:
                        logger.critical(f"Failed to send to dead letter queue: {dlq_error}")

                    return False

    # Usage
    messages = [
        {"id": "msg-1", "data": "test data 1"},
        {"id": "msg-2", "data": "test data 2"},
    ]

    for msg in messages:
        send_message_with_retry(msg)
```

### Consumer Error Handling

```python
import time
from collections import defaultdict
from quixstreams import Application

class CircuitBreaker:
    """Circuit breaker for consumer error handling"""

    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""

        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)

            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                logger.info("Circuit breaker reset to CLOSED")

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.error(f"Circuit breaker OPENED after {self.failure_count} failures")

            raise e

def resilient_consumer():
    """Consumer with comprehensive error handling"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="resilient-group",
        enable_auto_commit=False  # Manual offset management for error handling
    )

    topic = app.topic(name="events", value_deserializer="json")
    dead_letter_topic = app.topic(name="failed-events", value_serializer="json")

    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=30)
    error_counts = defaultdict(int)
    max_retries_per_message = 3

    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        while True:
            try:
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

                message_key = msg.key().decode() if msg.key() else "unknown"

                try:
                    # Use circuit breaker for processing
                    result = circuit_breaker.call(process_message, msg.value())

                    # Success - commit offset and reset error count
                    consumer.commit(msg)
                    error_counts[message_key] = 0
                    logger.debug(f"Successfully processed message: {message_key}")

                except Exception as processing_error:
                    error_counts[message_key] += 1

                    logger.error(f"Processing failed for {message_key} "
                               f"(attempt {error_counts[message_key]}): {processing_error}")

                    if error_counts[message_key] >= max_retries_per_message:
                        # Send to dead letter queue
                        failed_message = {
                            "original_key": message_key,
                            "original_value": msg.value().decode(),
                            "error": str(processing_error),
                            "failed_at": time.time(),
                            "attempts": error_counts[message_key],
                            "original_offset": msg.offset(),
                            "original_partition": msg.partition()
                        }

                        try:
                            with app.get_producer() as dlq_producer:
                                dlq_msg = dead_letter_topic.serialize(
                                    key=f"failed-{message_key}",
                                    value=failed_message
                                )
                                dlq_producer.produce(
                                    topic=dead_letter_topic.name,
                                    key=dlq_msg.key,
                                    value=dlq_msg.value
                                )
                                dlq_producer.flush()

                            logger.info(f"Sent message to dead letter queue: {message_key}")

                            # Commit offset to skip this message
                            consumer.commit(msg)
                            error_counts[message_key] = 0

                        except Exception as dlq_error:
                            logger.critical(f"Failed to send to dead letter queue: {dlq_error}")
                            # Don't commit - will retry
                    else:
                        # Don't commit offset - will retry this message
                        logger.info(f"Will retry message {message_key} "
                                   f"({max_retries_per_message - error_counts[message_key]} attempts left)")

            except KeyboardInterrupt:
                logger.info("Consumer interrupted by user")
                break
            except Exception as consumer_error:
                logger.error(f"Consumer error: {consumer_error}")
                time.sleep(5)  # Brief pause before retrying
```

## StreamingDataFrame (SDF) Processing

### StreamingDataFrame Overview (Assembly Line Analogy)

**StreamingDataFrame (SDF)** is QuixStreams' pandas-like interface for stream processing. Think of it as an **intelligent assembly line** where each message is a product moving through various processing stations.

#### 🏭 **Assembly Line Concept**

| Assembly Line           | StreamingDataFrame | Real Example                         |
| ----------------------- | ------------------ | ------------------------------------ |
| **Raw Materials**       | Input messages     | Sensor readings, user clicks, orders |
| **Processing Stations** | SDF operations     | Clean, transform, enrich, filter     |
| **Quality Control**     | Filtering          | Remove invalid data, outliers        |
| **Assembly Workers**    | Functions          | `apply()`, `update()`, `filter()`    |
| **Finished Products**   | Output messages    | Alerts, aggregated data, reports     |
| **Conveyor Belt**       | Kafka topics       | Continuous message flow              |

### Key SDF Features (Processing Capabilities)

- **🧩 Pandas-like API**: Familiar syntax for data transformations (like using familiar tools)
- **⚡ Real-time Processing**: Stream processing with low latency (assembly line never stops)
- **🕐 Windowing Operations**: Time-based and session-based windows (batch processing)
- **📊 Stateful Operations**: Aggregations and complex transformations (memory between items)
- **🔧 Column Operations**: Add, modify, and transform columns (add components)
- **🔍 Row Filtering**: Filter streams based on conditions (quality control)

### SDF Transformation Options (Assembly Line Stations)

| Operation  | Assembly Line Station | Input Type     | Output Type    | Example                    | Use Case              |
| ---------- | --------------------- | -------------- | -------------- | -------------------------- | --------------------- |
| `apply()`  | **Transformer**       | `function`     | Same/Different | Convert temperature units  | Data transformation   |
| `update()` | **Inspector**         | `function`     | Same           | Log processing, debug      | Side effects, logging |
| `filter()` | **Quality Control**   | `function`     | Subset         | Remove invalid readings    | Data validation       |
| `select()` | **Parts Picker**      | Column names   | Subset         | Keep only essential fields | Data projection       |
| `assign()` | **Component Adder**   | Column mapping | Extended       | Add calculated fields      | Feature engineering   |
| `drop()`   | **Parts Remover**     | Column names   | Subset         | Remove sensitive data      | Data privacy          |
| `expand()` | **Unpacker**          | Array column   | Multiple rows  | Split CSV into rows        | Data normalization    |

### Basic StreamingDataFrame Example (Simple Assembly Line)

```python
from quixstreams import Application

def simple_assembly_line():
    """Basic assembly line - process sensor readings"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sensor-processing-line",
    )

    # 📥 Raw materials input
    raw_sensor_topic = app.topic(name="raw-sensor-data", value_deserializer="json")

    # 🏭 Start the assembly line
    assembly_line = app.dataframe(topic=raw_sensor_topic)

    # 🔍 Station 1: Quality Inspection (log what's coming in)
    assembly_line = assembly_line.update(
        lambda reading: print(f"📥 Raw input: Sensor {reading['sensor_id']} = {reading['value']}")
    )

    # 🌡️ Station 2: Unit Conversion (transform Celsius to Fahrenheit)
    assembly_line["fahrenheit"] = assembly_line["celsius"].apply(lambda c: c * 9/5 + 32)

    # 🏷️ Station 3: Categorization (add labels)
    assembly_line["temperature_category"] = assembly_line["celsius"].apply(
        lambda temp: "🔥 HOT" if temp > 30 else "🌤️ WARM" if temp > 20 else "❄️ COOL"
    )

    # ✅ Station 4: Quality Control (filter out broken sensors)
    assembly_line = assembly_line.filter(
        lambda reading: reading["value"] >= -50 and reading["value"] <= 100
    )

    # 📤 Station 5: Final Inspection (log finished products)
    assembly_line = assembly_line.update(
        lambda processed: print(f"📤 Finished: {processed['sensor_id']} → {processed['temperature_category']}")
    )

    # 🏃‍♂️ Start the assembly line
    if __name__ == "__main__":
        print("🏭 Starting sensor processing assembly line...")
        app.run()
```

### Column Operations (Component Assembly)

```python
def component_assembly_example():
    """Advanced assembly line with multiple component stations"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="advanced-assembly-line",
    )

    # 📦 Input: Raw IoT device data
    input_topic = app.topic(name="iot-devices", value_deserializer="json")
    assembly_line = app.dataframe(topic=input_topic)

    print("🏭 Advanced IoT Assembly Line Starting...")

    # 🔧 Station 1: Add timestamp component
    from datetime import datetime
    assembly_line["processed_at"] = assembly_line.apply(
        lambda item: datetime.now().isoformat()
    )

    # 🌡️ Station 2: Temperature processing
    assembly_line["fahrenheit"] = assembly_line["celsius"].apply(lambda c: round(c * 9/5 + 32, 1))
    assembly_line["temp_status"] = assembly_line["celsius"].apply(
        lambda c: "🔥 CRITICAL" if c > 40 else "⚠️ WARNING" if c > 30 else "✅ NORMAL"
    )

    # 🔋 Station 3: Battery health assessment
    assembly_line["battery_health"] = assembly_line["battery_level"].apply(
        lambda level: "🔴 LOW" if level < 20 else "🟡 MEDIUM" if level < 50 else "🟢 GOOD"
    )

    # 📊 Station 4: Multi-component assembly (assign multiple at once)
    assembly_line = assembly_line.assign(
        device_status=assembly_line.apply(
            lambda row: "🚨 ALERT" if row["temp_status"] == "🔥 CRITICAL" or row["battery_health"] == "🔴 LOW" else "✅ OK"
        ),
        priority_score=assembly_line.apply(
            lambda row: 10 if "🔥" in row.get("temp_status", "") else 5 if "⚠️" in row.get("temp_status", "") else 1
        )
    )

    # 🎯 Station 5: Component selection (pick essential parts)
    assembly_line = assembly_line.select([
        "device_id", "celsius", "fahrenheit", "temp_status",
        "battery_level", "battery_health", "device_status",
        "priority_score", "processed_at"
    ])

    # 🗑️ Station 6: Remove internal components (privacy protection)
    assembly_line = assembly_line.drop(["internal_id", "raw_sensor_data", "debug_info"])

    # 📋 Final inspection
    assembly_line = assembly_line.update(
        lambda device: print(f"📋 Quality Check: Device {device['device_id']} → {device['device_status']}")
    )

    return assembly_line
```

### Filtering and Conditional Operations

```python
def filtering_operations_example():
    """Advanced filtering and conditional operations"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-filter-group",
    )

    input_topic = app.topic(name="events", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Basic filtering
    sdf = sdf.filter(lambda row: row["temperature"] > 0)  # Remove invalid readings
    sdf = sdf.filter(lambda row: row["user_id"] is not None)  # Ensure user ID exists

    # Complex conditional filtering
    sdf = sdf.filter(
        lambda row: (
            row["event_type"] in ["click", "view", "purchase"] and
            row["timestamp"] > "2024-01-01" and
            row.get("valid", True)
        )
    )

    # Conditional transformations
    sdf["priority"] = sdf.apply(
        lambda row: (
            "high" if row["event_type"] == "purchase" else
            "medium" if row["event_type"] == "click" else
            "low"
        )
    )

    # Filter based on computed values
    sdf = sdf.filter(lambda row: row["priority"] in ["high", "medium"])

    return sdf
```

### Array Expansion and Flattening

```python
def array_expansion_example():
    """Handle arrays and nested data structures"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-expand-group",
    )

    input_topic = app.topic(name="nested-data", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Example input: {"user_id": "123", "items": ["apple", "banana", "orange"]}

    # Expand array into separate rows
    sdf = sdf.apply(
        lambda row: [
            {"user_id": row["user_id"], "item": item, "original_count": len(row["items"])}
            for item in row["items"]
        ],
        expand=True
    )

    # Result: Multiple rows, one per item
    # {"user_id": "123", "item": "apple", "original_count": 3}
    # {"user_id": "123", "item": "banana", "original_count": 3}
    # {"user_id": "123", "item": "orange", "original_count": 3}

    # Add item-specific processing
    sdf["item_category"] = sdf["item"].apply(
        lambda item: "fruit" if item in ["apple", "banana", "orange"] else "other"
    )

    return sdf

def nested_data_flattening():
    """Flatten nested JSON structures"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-flatten-group",
    )

    input_topic = app.topic(name="complex-data", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Example input: {
    #   "user": {"id": "123", "name": "John", "address": {"city": "NYC", "zip": "10001"}},
    #   "order": {"id": "ord-456", "total": 99.99}
    # }

    # Flatten nested structure
    sdf = sdf.apply(lambda row: {
        "user_id": row["user"]["id"],
        "user_name": row["user"]["name"],
        "user_city": row["user"]["address"]["city"],
        "user_zip": row["user"]["address"]["zip"],
        "order_id": row["order"]["id"],
        "order_total": row["order"]["total"],
        "processed_at": time.time()
    })

    return sdf
```

### Windowing Operations

```python
def windowing_operations_example():
    """Time-based windowing with SDF"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-window-group",
    )

    input_topic = app.topic(name="time-series", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Tumbling window (non-overlapping)
    sdf = sdf.tumbling_window(duration_ms=60000)  # 1-minute windows

    # Aggregation within windows
    sdf = sdf.reduce(
        reducer=lambda acc, row: {
            "window_start": acc.get("window_start", row["timestamp"]),
            "count": acc.get("count", 0) + 1,
            "sum_value": acc.get("sum_value", 0) + row["value"],
            "max_value": max(acc.get("max_value", float("-inf")), row["value"]),
            "min_value": min(acc.get("min_value", float("inf")), row["value"]),
        },
        initializer=lambda: {}
    )

    # Calculate average
    sdf["avg_value"] = sdf.apply(
        lambda window: window["sum_value"] / window["count"] if window["count"] > 0 else 0
    )

    return sdf

def sliding_window_example():
    """Sliding window operations"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-sliding-group",
    )

    input_topic = app.topic(name="metrics", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Sliding window (overlapping)
    sdf = sdf.sliding_window(duration_ms=300000, step_ms=60000)  # 5-min window, 1-min step

    # Moving average calculation
    sdf = sdf.reduce(
        reducer=lambda acc, row: {
            "values": acc.get("values", []) + [row["metric_value"]],
            "timestamps": acc.get("timestamps", []) + [row["timestamp"]],
        },
        initializer=lambda: {}
    )

    # Calculate moving statistics
    sdf["moving_avg"] = sdf["values"].apply(lambda vals: sum(vals) / len(vals))
    sdf["moving_std"] = sdf["values"].apply(
        lambda vals: (sum((x - sum(vals)/len(vals))**2 for x in vals) / len(vals))**0.5
    )

    return sdf
```

### Stateful Processing

```python
def stateful_processing_example():
    """Stateful operations with SDF"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-stateful-group",
    )

    input_topic = app.topic(name="user-events", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Group by user and maintain state
    sdf = sdf.group_by("user_id")

    # Stateful reducer - track user session
    sdf = sdf.reduce(
        reducer=lambda acc, row: {
            "user_id": row["user_id"],
            "session_start": acc.get("session_start", row["timestamp"]),
            "last_activity": row["timestamp"],
            "event_count": acc.get("event_count", 0) + 1,
            "events": acc.get("events", []) + [row["event_type"]],
            "total_value": acc.get("total_value", 0) + row.get("value", 0),
        },
        initializer=lambda: {}
    )

    # Calculate session duration
    sdf["session_duration"] = sdf.apply(
        lambda session: session["last_activity"] - session["session_start"]
    )

    # Detect session patterns
    sdf["session_type"] = sdf["events"].apply(
        lambda events: (
            "purchase_session" if "purchase" in events else
            "browse_session" if "view" in events else
            "engagement_session"
        )
    )

    return sdf
```

### Error Handling in SDF

```python
def error_handling_sdf():
    """Error handling patterns in StreamingDataFrame"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-error-group",
    )

    input_topic = app.topic(name="raw-data", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Safe transformations with error handling
    def safe_transform(row):
        """Transform with error handling"""
        try:
            return {
                "id": row["id"],
                "value": float(row["value"]),
                "processed": True,
                "error": None
            }
        except (KeyError, ValueError, TypeError) as e:
            return {
                "id": row.get("id", "unknown"),
                "value": None,
                "processed": False,
                "error": str(e),
                "original": row
            }

    sdf = sdf.apply(safe_transform)

    # Filter successful transformations
    valid_sdf = sdf.filter(lambda row: row["processed"])
    error_sdf = sdf.filter(lambda row: not row["processed"])

    # Process valid data
    valid_sdf["computed"] = valid_sdf["value"].apply(lambda v: v * 2 if v else 0)

    # Log errors
    error_sdf = error_sdf.update(
        lambda row: logger.error(f"Processing error: {row['error']} for data: {row['original']}")
    )

    return valid_sdf, error_sdf
```

### Output and Sinks

```python
def sdf_output_example():
    """Different ways to output SDF results"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-output-group",
    )

    input_topic = app.topic(name="input-stream", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Process data
    sdf["enriched"] = sdf.apply(lambda row: {**row, "processed_at": time.time()})

    # Output to Kafka topic
    output_topic = app.topic(name="processed-stream", value_serializer="json")
    sdf = sdf.to_topic(output_topic)

    # Alternative: Print to console
    sdf = sdf.update(lambda row: print(f"Processed: {row}"))

    # Alternative: Custom sink function
    def send_to_database(row):
        """Custom sink to database"""
        # database.insert(row)
        print(f"Saved to DB: {row}")

    sdf = sdf.update(send_to_database)

    # Run the application
    if __name__ == "__main__":
        app.run()
```

### Complete SDF Pipeline Example

```python
import time
from datetime import datetime
from quixstreams import Application

def complete_sdf_pipeline():
    """Complete real-world SDF pipeline example"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="sdf-complete-pipeline",
        auto_offset_reset="earliest"
    )

    # Input: E-commerce events
    input_topic = app.topic(name="ecommerce-events", value_deserializer="json")
    sdf = app.dataframe(topic=input_topic)

    # Step 1: Data validation and cleaning
    sdf = sdf.filter(lambda row: all(key in row for key in ["user_id", "event_type", "timestamp"]))
    sdf = sdf.filter(lambda row: row["user_id"] is not None and row["event_type"] in ["view", "click", "purchase"])

    # Step 2: Data enrichment
    sdf["processed_at"] = sdf.apply(lambda row: datetime.now().isoformat())
    sdf["event_value"] = sdf.apply(lambda row: {
        "view": 1, "click": 5, "purchase": 100
    }.get(row["event_type"], 0))

    # Step 3: User session tracking (stateful)
    sdf = sdf.group_by("user_id")
    sdf = sdf.reduce(
        reducer=lambda acc, row: {
            "user_id": row["user_id"],
            "session_events": acc.get("session_events", 0) + 1,
            "session_value": acc.get("session_value", 0) + row["event_value"],
            "last_event": row["event_type"],
            "session_start": acc.get("session_start", row["timestamp"]),
            "session_end": row["timestamp"],
        },
        initializer=lambda: {}
    )

    # Step 4: Session analysis
    sdf["session_duration"] = sdf.apply(
        lambda session: session["session_end"] - session["session_start"]
    )
    sdf["session_quality"] = sdf.apply(lambda session:
        "high" if session["session_value"] > 50 else
        "medium" if session["session_value"] > 10 else
        "low"
    )

    # Step 5: Filtering and output
    high_value_sessions = sdf.filter(lambda session: session["session_quality"] == "high")

    # Output to different destinations
    output_topic = app.topic(name="user-sessions", value_serializer="json")
    high_value_sessions = high_value_sessions.to_topic(output_topic)

    # Real-time alerts for high-value sessions
    high_value_sessions = high_value_sessions.update(
        lambda session: print(f"HIGH VALUE SESSION ALERT: User {session['user_id']} - Value: {session['session_value']}")
    )

    # Run the pipeline
    if __name__ == "__main__":
        print("Starting SDF pipeline...")
        app.run()

# Run the complete example
if __name__ == "__main__":
    complete_sdf_pipeline()
```

### SDF Best Practices

1. **Use `update()` for Side Effects**: Use `update()` for logging, debugging, or sending alerts without changing the data
2. **Use `apply()` for Transformations**: Use `apply()` when you need to transform the data structure
3. **Filter Early**: Apply filters as early as possible to reduce processing load
4. **Handle Errors Gracefully**: Always include error handling in transformations
5. **Use Windowing for Aggregations**: Use appropriate windowing for time-based aggregations
6. **Optimize Column Operations**: Add computed columns efficiently
7. **Test with Small Data**: Test SDF pipelines with small datasets first
8. **Monitor Performance**: Keep track of processing rates and latencies

StreamingDataFrame provides a powerful, pandas-like interface for real-time stream processing, making complex data transformations intuitive and efficient.

## Advanced Features

### Production Best Practices (Real-World Operation)

QuixStreams provides advanced features for production deployments. Think of these as **professional-grade equipment** for your data processing operations.

#### 🏭 **Production Readiness Checklist**

| Feature            | Development (Backyard Setup)  | Production (Industrial Operation) |
| ------------------ | ----------------------------- | --------------------------------- |
| **Brokers**        | 1 broker (single post office) | 3+ brokers (multiple locations)   |
| **Replication**    | Factor 1 (no backup)          | Factor 3+ (multiple backups)      |
| **Monitoring**     | Basic logs                    | Comprehensive metrics             |
| **Error Handling** | Simple retries                | Circuit breakers + DLQ            |
| **Security**       | PLAINTEXT                     | SSL/SASL authentication           |
| **Scaling**        | Single consumer               | Consumer groups                   |

#### 🔧 **Advanced Configuration Examples**

```python
# 🏭 Production-grade application setup
production_app = Application(
    broker_address="prod-kafka-cluster:9092",
    consumer_group="production-processors",

    # 🛡️ Security settings
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_username="app-user",
    sasl_password="secure-password",

    # ⚡ Performance tuning
    request_timeout_ms=10000,
    auto_commit_enable=False,  # Manual offset control
    max_poll_records=500,      # Balanced batch size

    # 🔍 Monitoring
    loglevel="INFO"
)

# 🏗️ High-performance producer for bulk operations
bulk_app = Application(
    broker_address="bulk-kafka:9092",
    acks="all",                    # Full durability
    retries=5,                     # Robust retry policy
    batch_size=65536,              # 64KB batches
    linger_ms=200,                 # Wait for full batches
    compression_type="snappy",     # Fast compression
    enable_idempotence=True        # Exactly-once semantics
)
```

### 🧭 **Choosing the Right Approach (Decision Guide)**

#### **When to Use Each Pattern**

| Scenario                   | Recommended Approach        | Postal Analogy                | Code Pattern                       |
| -------------------------- | --------------------------- | ----------------------------- | ---------------------------------- |
| **Simple Data Pipeline**   | Basic Producer/Consumer     | Standard mail service         | Single topic, JSON serialization   |
| **High-Volume Processing** | Consumer Groups + Batching  | Mail sorting facility         | Multiple consumers, larger batches |
| **Real-time Analytics**    | StreamingDataFrame          | Assembly line processing      | SDF with windowing                 |
| **Critical Transactions**  | Manual Offsets + DLQ        | Registered mail with tracking | Manual commits, error handling     |
| **Development/Testing**    | Auto-commit + Latest offset | Casual mail checking          | Simple config, easy debugging      |

#### **Performance vs Reliability Trade-offs**

```python
# ⚡ SPEED-OPTIMIZED (for non-critical data)
speed_config = {
    "acks": 0,                     # No confirmation
    "enable_auto_commit": True,    # Auto-commit offsets
    "auto_offset_reset": "latest", # Skip old data
    "batch_size": 65536,           # Large batches
    "linger_ms": 0                 # Send immediately
}

# 🛡️ RELIABILITY-OPTIMIZED (for critical data)
reliability_config = {
    "acks": "all",                    # Full confirmation
    "enable_auto_commit": False,      # Manual control
    "auto_offset_reset": "earliest",  # Process all data
    "retries": 10,                    # Many retries
    "enable_idempotence": True        # Prevent duplicates
}

# ⚖️ BALANCED (for most use cases)
balanced_config = {
    "acks": 1,                     # Leader confirmation
    "enable_auto_commit": True,    # Convenience
    "auto_offset_reset": "latest", # Recent data
    "retries": 3,                  # Some resilience
    "batch_size": 32768            # Moderate batching
}
```

### 🚀 **Getting Started Recommendations**

#### **For Beginners** (Learning Setup)

1. **Start Simple**: Use Docker Compose setup with 1 partition
2. **Use JSON**: Stick with JSON serialization for readability
3. **Auto-commit**: Let Kafka handle offset management
4. **Latest offset**: Focus on new messages only
5. **Debug heavily**: Use lots of `update()` operations to see data flow

#### **For Production** (Professional Setup)

1. **Plan Partitions**: Calculate partition count based on throughput needs
2. **Manual Offsets**: Control exactly-once processing with manual commits
3. **Monitor Everything**: Implement comprehensive logging and metrics
4. **Error Handling**: Set up dead letter queues and circuit breakers
5. **Security**: Enable SSL/SASL for production clusters

#### **Common Pitfalls and Solutions**

| Problem                  | Postal Analogy              | Solution                            |
| ------------------------ | --------------------------- | ----------------------------------- |
| **Lost Messages**        | Mail truck crashed          | Use `acks="all"` + retries          |
| **Duplicate Processing** | Same letter delivered twice | Enable idempotence + manual commits |
| **Consumer Lag**         | Mail piling up              | Add more consumers to group         |
| **Offset Reset Issues**  | Wrong starting mailbox      | Use consistent `auto_offset_reset`  |
| **Partition Imbalance**  | One mail carrier overloaded | Use round-robin key assignment      |

### 📚 **Quick Reference (Cheat Sheet)**

#### **Essential Configuration Combinations**

```python
# 📊 ANALYTICS WORKLOAD (process all historical data)
analytics_app = Application(
    broker_address="localhost:9092",
    consumer_group="analytics-team",
    auto_offset_reset="earliest",  # Read all history
    enable_auto_commit=True,       # Convenience for batch jobs
    max_poll_records=1000          # Large batches for efficiency
)

# 🚨 REAL-TIME ALERTS (only new events matter)
alerts_app = Application(
    broker_address="localhost:9092",
    consumer_group="alert-system",
    auto_offset_reset="latest",    # Only new events
    enable_auto_commit=False,      # Manual control for reliability
    max_poll_interval_ms=30000     # Quick failure detection
)

# 🔄 DATA MIGRATION (reliable transfer)
migration_app = Application(
    broker_address="localhost:9092",
    consumer_group="data-migration",
    auto_offset_reset="earliest",     # Process everything
    enable_auto_commit=False,         # Manual offset control
    acks="all",                       # Full durability
    enable_idempotence=True           # No duplicates
)
```

Remember: **Start simple, then optimize**. Like learning to drive - begin in an empty parking lot (development) before hitting the highway (production)! 🚗

---

_This guide uses postal service and assembly line analogies to make Kafka concepts intuitive. Each technical concept has a real-world parallel to help you understand not just the "what" but the "why" behind Kafka's design._

### Multiple Topics and Routing

```python
def multi_topic_consumer_with_routing():
    """Consumer handling multiple topics with intelligent routing"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="multi-topic-group"
    )

    # Define multiple topics
    topics = {
        "user-events": app.topic(name="user-events", value_deserializer="json"),
        "system-events": app.topic(name="system-events", value_deserializer="json"),
        "error-events": app.topic(name="error-events", value_deserializer="json")
    }

    # Topic-specific processors
    processors = {
        "user-events": process_user_event,
        "system-events": process_system_event,
        "error-events": process_error_event
    }

    with app.get_consumer() as consumer:
        consumer.subscribe(list(topics.keys()))

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                continue

            topic_name = msg.topic()

            if topic_name in topics and topic_name in processors:
                try:
                    # Deserialize using topic-specific deserializer
                    deserialized = topics[topic_name].deserialize(msg)

                    # Route to topic-specific processor
                    processor = processors[topic_name]
                    result = processor(deserialized.value)

                    logger.info(f"Processed {topic_name} message: {result}")

                except Exception as e:
                    logger.error(f"Failed to process {topic_name} message: {e}")
            else:
                logger.warning(f"Unknown topic: {topic_name}")

def process_user_event(event):
    """Process user-specific events"""
    logger.info(f"Processing user event: {event.get('user_id')}")
    return {"status": "user_processed", "user_id": event.get("user_id")}

def process_system_event(event):
    """Process system events"""
    logger.info(f"Processing system event: {event.get('event_type')}")
    return {"status": "system_processed", "event_type": event.get("event_type")}

def process_error_event(event):
    """Process error events"""
    logger.error(f"Processing error event: {event.get('error_code')}")
    return {"status": "error_processed", "error_code": event.get("error_code")}
```

### Stream Processing with DataFrames

```python
from quixstreams import Application
import pandas as pd

def stream_processing_example():
    """Advanced stream processing using QuixStreams DataFrame API"""

    app = Application(
        broker_address="localhost:9092",
        consumer_group="stream-processing-group"
    )

    # Define input topic
    input_topic = app.topic(name="sensor-data", value_deserializer="json")

    # Define stream processing pipeline
    sdf = app.dataframe(input_topic)

    # Add transformations
    sdf = sdf.filter(lambda x: x["temperature"] > 0)  # Filter invalid readings
    sdf = sdf.apply(lambda x: {
        **x,
        "celsius_to_fahrenheit": x["temperature"] * 9/5 + 32,
        "timestamp": pd.Timestamp.now().isoformat()
    })

    # Group by sensor and calculate moving average
    sdf = sdf.tumbling_window(duration_ms=60000)  # 1-minute windows
    sdf = sdf.reduce(
        reducer=lambda acc, x: {
            "sensor_id": x["sensor_id"],
            "avg_temperature": (acc.get("avg_temperature", 0) + x["temperature"]) / 2,
            "count": acc.get("count", 0) + 1,
            "window_start": acc.get("window_start", x["timestamp"])
        },
        initializer=lambda: {}
    )

    # Output to new topic
    output_topic = app.topic(name="processed-sensor-data", value_serializer="json")
    sdf = sdf.to_topic(output_topic)

    # Run the pipeline
    app.run(sdf)

def custom_serialization_example():
    """Example with custom serialization for complex data types"""

    import pickle
    import json
    from datetime import datetime

    app = Application(broker_address="localhost:9092")

    # Custom serialization functions
    def serialize_complex(obj):
        """Serialize complex Python objects"""
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        elif isinstance(obj, set):
            return {"__set__": list(obj)}
        elif hasattr(obj, "__dict__"):
            return {"__object__": obj.__dict__, "__class__": obj.__class__.__name__}
        else:
            return pickle.dumps(obj).hex()

    def deserialize_complex(data):
        """Deserialize complex Python objects"""
        if isinstance(data, dict):
            if "__datetime__" in data:
                return datetime.fromisoformat(data["__datetime__"])
            elif "__set__" in data:
                return set(data["__set__"])
            elif "__object__" in data:
                # Reconstruct object (simplified)
                return data["__object__"]

        try:
            return pickle.loads(bytes.fromhex(data))
        except:
            return data

    # Topic without built-in serialization
    topic = app.topic(name="complex-data")

    # Producer
    with app.get_producer() as producer:
        complex_data = {
            "timestamp": datetime.now(),
            "tags": {"important", "processed", "validated"},
            "metadata": {"version": 1.0, "source": "sensor-array"}
        }

        # Custom serialization
        serialized_data = json.dumps(complex_data, default=serialize_complex)

        producer.produce(
            topic=topic.name,
            key=b"complex-data-1",
            value=serialized_data.encode()
        )
        producer.flush()

    # Consumer
    with app.get_consumer() as consumer:
        consumer.subscribe([topic.name])

        msg = consumer.poll(timeout=5.0)
        if msg and not msg.error():
            # Custom deserialization
            raw_data = msg.value().decode()
            deserialized_data = json.loads(raw_data, object_hook=lambda d: deserialize_complex(d))

            logger.info(f"Deserialized complex data: {deserialized_data}")
```

### Production Configuration Template

```python
def create_production_application(env="production"):
    """Create a production-ready QuixStreams application"""

    config = {
        "development": {
            "broker_address": "localhost:9092",
            "loglevel": "DEBUG",
            "auto_offset_reset": "earliest"
        },
        "staging": {
            "broker_address": "staging-kafka:9092",
            "loglevel": "INFO",
            "auto_offset_reset": "latest",
            "security_protocol": "SASL_PLAINTEXT"
        },
        "production": {
            "broker_address": "prod-kafka:9092",
            "loglevel": "WARNING",
            "auto_offset_reset": "latest",
            "security_protocol": "SASL_SSL",
            "sasl_mechanism": "PLAIN",
            "enable_auto_commit": False,
            "acks": "all",
            "retries": 5,
            "enable_idempotence": True,
            "compression_type": "gzip",
            "batch_size": 32768,
            "linger_ms": 100
        }
    }

    app_config = config.get(env, config["development"])

    # Add credentials from environment
    import os
    if env in ["staging", "production"]:
        app_config.update({
            "sasl_username": os.getenv("KAFKA_USERNAME"),
            "sasl_password": os.getenv("KAFKA_PASSWORD")
        })

    app = Application(
        consumer_group=f"app-{env}",
        **app_config
    )

    logger.info(f"Created {env} application with config: {app_config}")
    return app

# Usage
prod_app = create_production_application("production")
dev_app = create_production_application("development")
```

This comprehensive guide provides all the configuration options, patterns, and best practices for using QuixStreams effectively in different scenarios. Each section includes detailed tables, practical examples, and production-ready code patterns.
