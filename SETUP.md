# Kafka Learning Project Setup and Installation Guide

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Apache Kafka** running locally or accessible remotely
3. **Git** for version control

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd learn-kafka

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Kafka configuration
# Update KAFKA_BOOTSTRAP_SERVERS if needed
```

### 3. Start Kafka (if running locally)

#### Using Kafka Binary:

```bash
# Start Zookeeper
bin\windows\zookeeper-server-start.bat config\zookeeper.properties

# Start Kafka Server
bin\windows\kafka-server-start.bat config\server.properties

# Create topic (optional - will be created automatically)
bin\windows\kafka-topics.bat --create --topic learn-kafka-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

#### Using Docker:

```bash
# Create docker-compose.yml and run
docker-compose up -d
```

### 4. Run the Project

```bash
# Run main application
python main.py

# Or install and run as package
pip install -e .
learn-kafka
```

## Project Structure

```
learn-kafka/
├── producer/           # Kafka producer examples
├── consumer/           # Kafka consumer examples
├── kafka_streams/      # Kafka streams examples
├── config/             # Configuration files
├── utils/              # Utility functions
├── main.py            # Main entry point
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project configuration
└── .env.example       # Environment variables template
```

## Development Setup

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Code Formatting and Linting

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Run tests
pytest
```

## Troubleshooting

### Common Issues:

1. **Cannot connect to Kafka**

   - Ensure Kafka is running on the configured port
   - Check KAFKA_BOOTSTRAP_SERVERS in .env file

2. **Topic not found**

   - Topics will be created automatically
   - Or create manually using kafka-topics command

3. **Permission errors**
   - Ensure proper file permissions
   - Run with appropriate user privileges

### Environment Variables

All configuration is managed through environment variables. See `.env.example` for all available options.

### Logs

The application uses colored logging. Check console output for debugging information.

## Next Steps

1. Implement producer examples in `producer/`
2. Implement consumer examples in `consumer/`
3. Add Kafka streams processing in `kafka_streams/`
4. Experiment with different serialization formats
5. Add error handling and monitoring
