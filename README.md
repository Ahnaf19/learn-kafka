# Learn Kafka with Python

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![QuixStreams](https://img.shields.io/badge/QuixStreams-3.21.0-orange.svg)](https://quix.io/docs/quix-streams/introduction.html)
[![Loguru](https://img.shields.io/badge/Loguru-0.7.3-green.svg)](https://loguru.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [!WARNING]  
> This project requires Docker to be installed and running for the Kafka broker setup.

> [!NOTE]
> Make sure you have Python 3.8+ installed before proceeding with the setup.

A comprehensive learning project for Apache Kafka using Python with QuixStreams, featuring modular message processing, Docker Compose setup, and cross-platform support.

## Features

- 🐍 **Python-based Kafka learning environment** with modern libraries
- 🚀 **QuixStreams integration** for efficient Kafka operations
- 🐳 **Docker Compose setup** for easy Kafka broker deployment
- 🔧 **Modular architecture** with reusable message handling classes
- 📝 **Comprehensive logging** using Loguru
- 🌍 **Cross-platform support** (Windows, macOS, Linux)
- 📚 **Detailed documentation** and usage guides

## Quick Start

1. **Clone and navigate to the project**:

   ```bash
   cd learn-kafka
   ```

2. **Set up your Python environment**:

   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Start Kafka with Docker**:

   ```bash
   docker-compose up -d
   ```

4. **Run the producer**:

   ```bash
   python producer/simple_producer.py
   ```

5. **Run the consumer** (in another terminal):
   ```bash
   python consumer/simple_consumer.py
   ```

## Project Structure

```
learn-kafka/
├── producer/
│   └── simple_producer.py      # QuixStreams-based message producer
├── consumer/
│   └── simple_consumer.py      # Consumer with modular message processing
├── utils/
│   └── kafka_message_handler.py # Modular message handling classes
├── docker-compose.yml          # Kafka broker setup
├── requirements.txt            # Python dependencies
├── SETUP.md                   # Detailed setup guide
├── QUIXSTREAMS_GUIDE.md       # QuixStreams usage documentation
└── README.md                  # This file
```

## Documentation

- **[Setup Guide](SETUP.md)** - Complete installation and configuration instructions
- **[QuixStreams Guide](QUIXSTREAMS_GUIDE.md)** - Comprehensive QuixStreams usage patterns and examples

## Core Components

```
Simple Producer → weather_data_demo → Simple Consumer → Simple Streamer → weather_i18n → (can consume data!)
      ↓                ↓                ↓                    ↓                  ↓
[produces data]     [topic]      [consumes data] [transforms+streams data]  [stream topic]
```

### Message Producer

The `simple_producer.py` demonstrates:

- QuixStreams Application setup
- JSON message serialization
- Weather data simulation
- Error handling and logging

### Message Consumer

The `simple_consumer.py` showcases:

- Consumer group configuration
- Message polling and processing
- Integration with modular message handlers
- Robust error handling

### Message Handler Classes

Located in `utils/kafka_message_handler.py`:

- **`KafkaMessageHandler`** - Base message processing with validation
- **`TopicAwareMessageHandler`** - Topic-specific message routing and handling

## Technology Stack

- **[Python 3.8+](https://python.org)** - Core runtime environment
- **[QuixStreams 3.21.0](https://quix.io/docs/quix-streams/)** - Modern Kafka Python client
- **[Loguru 0.7.3](https://loguru.readthedocs.io/)** - Enhanced logging capabilities
- **[Docker Compose](https://docs.docker.com/compose/)** - Containerized Kafka infrastructure
- **[Apache Kafka](https://kafka.apache.org/)** - Distributed streaming platform

## Learning Objectives

This project helps you understand:

1. **Kafka Fundamentals**

   - Producer and consumer patterns
   - Topic management and partitioning
   - Message serialization/deserialization

2. **QuixStreams Library**

   - Application configuration
   - Message handling and processing
   - Error handling and retries

3. **Python Best Practices**

   - Modular code organization
   - Class-based message processing
   - Comprehensive logging strategies

4. **Development Environment**
   - Docker Compose for local development
   - Virtual environment management
   - Cross-platform compatibility

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit with descriptive messages
5. Push to your fork and submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [QuixStreams Installatioun](https://pypi.org/project/quixstreams/)
- [QuixStreams Documentation](https://quix.io/docs/quix-streams/introduction.html#next-steps)
- [DockerHub apache/kafka](https://hub.docker.com/r/apache/kafka)
- [Python Kafka Tutorial](https://kafka-python.readthedocs.io/)
- [Docker Compose for Kafka](https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html)

---

**Happy Learning!** 🎓 Start with the [Setup Guide](SETUP.md) to get your environment ready.
