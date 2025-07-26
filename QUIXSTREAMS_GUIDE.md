# QuixStreams Kafka Quick Guide

## What is Apache Kafka?

**Apache Kafka** is a distributed streaming platform that **decouples data producers and consumers**, eliminating the need for direct communication between systems. Instead of services talking directly to each other, they communicate through Kafka topics.

**Key Benefits:**

- **Decoupling**: Producers and consumers don't need to know about each other
- **Scalability**: Handle millions of messages per second across multiple machines
- **Durability**: Messages are persisted and replicated for fault tolerance
- **Real-time**: Low-latency message delivery for real-time applications

## Core Concepts

| Component          | What It Is                                | How It Works                                       | Client Control                          |
| ------------------ | ----------------------------------------- | -------------------------------------------------- | --------------------------------------- |
| **Topic**          | Named message category                    | Like a mailbox for specific data types             | ✅ Create, configure, delete            |
| **Partition**      | Topic subdivision for parallel processing | Multiple lanes in a topic for load distribution    | ⚙️ Set count during topic creation      |
| **Offset**         | Message position number in partition      | Sequential ID (0, 1, 2...) for message ordering    | 📖 Read from specific positions         |
| **Producer**       | Application that sends messages           | Writes data to topics, chooses partitioning        | ✅ Full control over what/where to send |
| **Consumer**       | Application that reads messages           | Reads from topics, tracks progress                 | ✅ Choose topics, manage offsets        |
| **Broker**         | Kafka server instance                     | Stores and serves messages                         | ❌ Infrastructure level                 |
| **Consumer Group** | Team of consumers sharing workload        | Automatically distributes partitions among members | ✅ Join groups, coordinate processing   |

## Kafka with Docker

```yaml
# docker-compose.yml
services:
  kafka:
    image: apache/kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://host.docker.internal:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

```bash
# Commands
docker-compose up -d     # Start Kafka
docker-compose down      # Stop (data preserved)
docker-compose down -v   # Stop and delete all data
```

**Data Persistence**: Kafka stores data in Docker volumes. Stopping containers preserves data, but `down -v` deletes everything.

## Python Kafka Clients

| Feature               | kafka-python | confluent-kafka | QuixStreams  |
| --------------------- | ------------ | --------------- | ------------ |
| **Performance**       | Moderate     | High            | High         |
| **Ease of Use**       | Complex      | Moderate        | **Simple**   |
| **Stream Processing** | None         | Basic           | **Advanced** |
| **Learning Curve**    | Steep        | Moderate        | **Gentle**   |

**Why QuixStreams?** Simplified API, built-in stream processing, automatic error handling, modern Python features.

## Application Configuration

| Option               | Values                                      | Default    | Description                       |
| -------------------- | ------------------------------------------- | ---------- | --------------------------------- |
| `broker_address`     | `"host:port"`                               | Required   | Kafka connection string           |
| `consumer_group`     | `"any-string"`                              | Required   | Consumer group identifier         |
| `auto_offset_reset`  | `"earliest"`, `"latest"`                    | `"latest"` | Where new consumers start reading |
| `loglevel`           | `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"` | `"INFO"`   | Logging verbosity                 |
| `auto_commit_enable` | `True`, `False`                             | `True`     | Automatic offset commits          |

```python
from quixstreams import Application

# Basic setup
app = Application(
    broker_address="localhost:9092",
    consumer_group="my-group",
    auto_offset_reset="earliest"  # Read all messages from start
)
```

## Producer Setup

| Option             | Values                                  | Default      | Description                 |
| ------------------ | --------------------------------------- | ------------ | --------------------------- |
| `acks`             | `0`, `1`, `"all"`                       | `1`          | Delivery confirmation level |
| `retries`          | `0-∞`                                   | `2147483647` | Retry attempts on failure   |
| `batch_size`       | bytes                                   | `16384`      | Message batching size       |
| `compression_type` | `"none"`, `"gzip"`, `"snappy"`, `"lz4"` | `"none"`     | Message compression         |

```python
# Basic producer
app = Application(broker_address="localhost:9092")
topic = app.topic(name="events", value_serializer="json")

with app.get_producer() as producer:
    message = {"user_id": 123, "action": "login"}
    kafka_msg = topic.serialize(key="user-123", value=message)
    producer.produce(topic=topic.name, key=kafka_msg.key, value=kafka_msg.value)
    producer.flush()  # Ensure delivery
```

## Consumer Setup

| Option                  | Values       | Default | Description              |
| ----------------------- | ------------ | ------- | ------------------------ |
| `max_poll_records`      | `1-∞`        | `500`   | Messages per poll        |
| `session_timeout_ms`    | milliseconds | `10000` | Consumer session timeout |
| `heartbeat_interval_ms` | milliseconds | `3000`  | Heartbeat frequency      |
| `fetch_min_bytes`       | bytes        | `1`     | Minimum fetch size       |

```python
# Basic consumer
app = Application(
    broker_address="localhost:9092",
    consumer_group="processors"
)
topic = app.topic(name="events", value_deserializer="json")

with app.get_consumer() as consumer:
    consumer.subscribe([topic.name])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg and not msg.error():
            print(f"Received: {msg.value()}")
```

## Topic Management

| Option               | Values                                | Default | Description               |
| -------------------- | ------------------------------------- | ------- | ------------------------- |
| `value_serializer`   | `"json"`, `"str"`, `"bytes"`, `"int"` | `None`  | Data format for sending   |
| `value_deserializer` | `"json"`, `"str"`, `"bytes"`, `"int"` | `None`  | Data format for receiving |
| `num_partitions`     | `1-∞`                                 | `1`     | Number of partitions      |
| `replication_factor` | `1-∞`                                 | `1`     | Replication copies        |

```python
# Topic configuration
json_topic = app.topic(
    name="user-events",
    value_serializer="json",    # For producers
    key_serializer="str"
)

consumer_topic = app.topic(
    name="user-events",
    value_deserializer="json",  # For consumers
    key_deserializer="str"
)
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

```python
def process_message(msg, topic):
    """Standard message processing pattern"""

    if msg is None or msg.error():
        return None

    # Get message components
    key = msg.key().decode('utf-8') if msg.key() else None
    value = topic.deserialize(msg).value
    offset = msg.offset()
    partition = msg.partition()

    # Process your business logic here
    processed_data = transform_data(value)

    return {
        "key": key,
        "data": processed_data,
        "metadata": {"offset": offset, "partition": partition}
    }
```

## Offset Management

### 🔢 **Offset Behavior Explained**

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

Strategies:

| Strategy          | When to Use         | Auto Commit | Manual Control          |
| ----------------- | ------------------- | ----------- | ----------------------- |
| **Auto Commit**   | Standard processing | ✅ `True`   | ❌ Limited              |
| **Manual Commit** | Critical data       | ❌ `False`  | ✅ Full control         |
| **Earliest**      | Replay all data     | N/A         | Set `auto_offset_reset` |
| **Latest**        | Real-time only      | N/A         | Set `auto_offset_reset` |

```python
# Manual offset management
app = Application(
    broker_address="localhost:9092",
    consumer_group="critical-processor",
    enable_auto_commit=False  # Manual control
)

with app.get_consumer() as consumer:
    consumer.subscribe([topic.name])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg and not msg.error():
            try:
                process_message(msg)
                consumer.commit(msg)  # Commit only after success
            except Exception as e:
                print(f"Processing failed: {e}")
                # Don't commit - will reprocess after restart
```

## Consumer Groups

**Purpose**: Load balancing and fault tolerance

| Scenario                   | Same Group                        | Different Groups                |
| -------------------------- | --------------------------------- | ------------------------------- |
| **Load Balancing**         | ✅ Multiple consumers share work  | ❌ All get same messages        |
| **Independent Processing** | ❌ Work is divided                | ✅ Each group processes all     |
| **Fault Tolerance**        | ✅ Others take over failed member | ✅ Groups operate independently |

### Consumer Group Configuration

| Option                          | Description         | Default Value | Example             | Team Analogy         |
| ------------------------------- | ------------------- | ------------- | ------------------- | -------------------- |
| `consumer_group`                | Consumer group ID   | Required      | `"processing-team"` | Team name badge      |
| `session_timeout_ms`            | Session timeout     | `10000`       | `30000`             | "Check-in" frequency |
| `heartbeat_interval_ms`         | Heartbeat frequency | `3000`        | `1000`              | "I'm alive" signals  |
| `max_poll_interval_ms`          | Max processing time | `300000`      | `60000`             | Max time per task    |
| `partition_assignment_strategy` | Assignment strategy | `"range"`     | `"roundrobin"`      | How to divide work   |

```python
# Same group (load balancing)
worker1 = Application(broker_address="localhost:9092", consumer_group="team-a")
worker2 = Application(broker_address="localhost:9092", consumer_group="team-a")
# Partitions split between worker1 and worker2

# Different groups (independent processing)
alerts = Application(broker_address="localhost:9092", consumer_group="alerts")
analytics = Application(broker_address="localhost:9092", consumer_group="analytics")
# Both process all messages independently
```

## Serialization

| Format    | Input Type     | Use Case        | Example                           |
| --------- | -------------- | --------------- | --------------------------------- |
| `"json"`  | `dict`, `list` | Structured data | `{"user": "alice", "score": 100}` |
| `"str"`   | `str`          | Text messages   | `"User login event"`              |
| `"bytes"` | `bytes`        | Binary data     | `b"raw file data"`                |
| `"int"`   | `int`          | Numeric values  | `42`                              |

```python
# Producer with JSON serialization
producer_topic = app.topic(name="events", value_serializer="json")

# Consumer with JSON deserialization
consumer_topic = app.topic(name="events", value_deserializer="json")
```

## StreamingDataFrame (SDF) Processing

**StreamingDataFrame (SDF)** is QuixStreams' pandas-like interface for stream processing and real-time data transformation.

### Key SDF Features (Processing Capabilities)

- **🧩 Pandas-like API**: Familiar syntax for data transformations (like using familiar tools)
- **⚡ Real-time Processing**: Stream processing with low latency (assembly line never stops)
- **🕐 Windowing Operations**: Time-based and session-based windows (batch processing)
- **📊 Stateful Operations**: Aggregations and complex transformations (memory between items)
- **🔧 Column Operations**: Add, modify, and transform columns (add components)
- **🔍 Row Filtering**: Filter streams based on conditions (quality control)

### SDF Transformation Options

| Operation    | Method                                                  | Input Type     | Output Type        | Description                    | Example                   | Use Case               |
| ------------ | ------------------------------------------------------- | -------------- | ------------------ | ------------------------------ | ------------------------- | ---------------------- |
| **Read**     | `sdf = app.dataframe(topic)`                            | Topic          | StreamingDataFrame | Create stream from topic       | Start pipeline            | Initial data ingestion |
| **Filter**   | `sdf.filter(lambda row: row["temp"] > 20)`              | Function       | Subset             | Keep rows matching condition   | Remove invalid readings   | Data validation        |
| **Apply**    | `sdf.apply(lambda row: row["value"] * 2)`               | Function       | Same/Different     | Modify each row                | Convert temperature units | Data transformation    |
| **Update**   | `sdf.update(lambda row: row.update({"new": "field"}))`  | Function       | Same               | Add/modify fields in-place     | Log processing, debug     | Side effects, logging  |
| **Select**   | `sdf.select("field1", "field2")`                        | Column names   | Subset             | Keep only specified fields     | Keep essential fields     | Data projection        |
| **Assign**   | `sdf.assign(new_field=lambda row: row["x"] + row["y"])` | Column mapping | Extended           | Add calculated fields          | Add computed values       | Feature engineering    |
| **Drop**     | `sdf.drop("sensitive_field")`                           | Column names   | Subset             | Remove specified fields        | Remove sensitive data     | Data privacy           |
| **Expand**   | `sdf.expand("array_field")`                             | Array column   | Multiple rows      | Split array into separate rows | Split CSV into rows       | Data normalization     |
| **Group By** | `sdf.group_by("user_id").count()`                       | Key field      | Aggregated         | Aggregate by key               | User activity counts      | Data aggregation       |
| **Window**   | `sdf.tumbling_window(duration_ms=60000)`                | Time duration  | Windowed           | Time-based aggregation         | Minute-by-minute metrics  | Temporal analysis      |
| **To Topic** | `sdf.to_topic(output_topic)`                            | Topic          | None               | Send results to topic          | Output processed data     | Data output            |

```python
# SDF Pipeline Example
app = Application(broker_address="localhost:9092", consumer_group="stream-processor")

input_topic = app.topic("raw-events", value_deserializer="json")
output_topic = app.topic("processed-events", value_serializer="json")

# Create streaming pipeline
sdf = app.dataframe(input_topic)
sdf = sdf.filter(lambda row: row["status"] == "active")          # Filter
sdf = sdf.apply(lambda row: {**row, "processed_at": time.time()}) # Transform
sdf = sdf.to_topic(output_topic)                                 # Output

# Run the pipeline
app.run(sdf)  # Processes messages in real-time
```

## Best Practices

### Quick Producer-Consumer Pipeline

```python
from quixstreams import Application

# 1. Setup application
app = Application(
    broker_address="localhost:9092",
    consumer_group="pipeline"
)

# 2. Define topics
input_topic = app.topic("raw-data", value_deserializer="json")
output_topic = app.topic("processed-data", value_serializer="json")

# 3. Create processing pipeline
sdf = app.dataframe(input_topic)
sdf = sdf.filter(lambda x: x["valid"] == True)
sdf = sdf.apply(lambda x: {"result": x["value"] * 2, "timestamp": time.time()})
sdf = sdf.to_topic(output_topic)

# 4. Run
app.run(sdf)
```

### Error Handling

```python
try:
    app.run(sdf)
except KeyboardInterrupt:
    print("Shutting down gracefully...")
except Exception as e:
    logger.error(f"Pipeline error: {e}")
    # Handle restart logic
```

### Production Considerations

| Aspect          | Recommendation                   | Configuration                  |
| --------------- | -------------------------------- | ------------------------------ |
| **Reliability** | Manual commits for critical data | `enable_auto_commit=False`     |
| **Performance** | Increase batch sizes             | `batch_size=32768`             |
| **Monitoring**  | Structured logging               | Custom logger setup            |
| **Security**    | Use SSL/SASL                     | `security_protocol="SASL_SSL"` |
| **Scaling**     | Multiple consumer instances      | Same `consumer_group`          |

### Common Patterns

```python
# Pattern 1: Data Enrichment
sdf = sdf.apply(lambda row: enrich_with_metadata(row))

# Pattern 2: Filtering Bad Data
sdf = sdf.filter(lambda row: validate_schema(row))

# Pattern 3: Format Transformation
sdf = sdf.apply(lambda row: convert_format(row))

# Pattern 4: Real-time Aggregation
sdf = sdf.group_by("user_id").tumbling_window(60000).count()
```

This concise guide focuses on practical usage patterns and essential configurations. Use the tables to understand available options, then apply them to the code examples based on your specific use case.
