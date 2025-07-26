# Project Setup Guide

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Installing Dependencies](#installing-dependencies)
- [Python Path Configuration](#python-path-configuration)
- [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8+
- Docker and Docker Compose or docker desktop
- Git (for cloning the repository)

## Environment Setup

### Option 1: Using Python venv

```bash
# Create virtual environment
# Windows
python -m venv kafka-env

# macOS/Linux
python3 -m venv kafka-env

# Activate virtual environment
# Windows (Command Prompt)
kafka-env\Scripts\activate

# Windows (PowerShell)
kafka-env\Scripts\Activate.ps1

# macOS/Linux
source kafka-env/bin/activate
```

### Option 2: Using Conda

```bash
# Create conda environment
conda create -n kafka-env python=3.11

# Activate conda environment
# Windows/macOS/Linux
conda activate kafka-env
```

## Installing Dependencies

After activating your virtual environment:

```bash
# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

## Python Path Configuration

To ensure proper module imports, add the project root to your Python path:

```bash
# linux or macOS
export PYTHONPATH=.

# windows
$env:PYTHONPATH = "." # powershell
set PYTHONPATH=. # cmd
```

## Docker Setup

### Starting Kafka

The project uses Docker Compose to run Kafka. Start the Kafka broker:

```bash
# Start Kafka in detached mode
docker-compose up -d

# View logs (optional)
docker-compose logs -f

# Check status
docker-compose ps

# Shutdown Kafka
docker-compose down
```

### Kafka Services

The Docker setup provides:

- **Kafka Broker**: `localhost:9092`
- **Internal networking**: `host.docker.internal:9092`

### Creating Topics (Optional)

> [!WARNING]
> Docker image `apache/kafka:latest` is a minimal base image and does not include CLI tools like `kafka-topics.sh`. So the below command will not work, try with `bitnami/kafka` or `confluentinc/cp-kafka`

Topics will be created automatically in python scripts, but you can create them manually:

```bash
# Access Kafka container
docker exec -it broker bash

# Create topic
kafka-topics.sh --create \
  --topic weather_data_demo \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Running the Application

### Producer

```bash
python producer/simple_producer.py
```

### Consumer

```bash
python consumer/simple_consumer.py
```

### End-to-End workflow

1. Start Kafka: `docker-compose up -d`
2. Run producer: `python producer/simple_producer.py`
3. Run consumer: `python consumer/simple_consumer.py`
4. Verify messages are being produced and consumed

## Development Notes

### Project Structure

```
learn-kafka/
├── producer/           # Producer scripts
├── consumer/           # Consumer scripts
├── utils/              # Utility modules
├── docker-compose.yml  # Kafka setup
├── requirements.txt    # Python dependencies
└── SETUP.md           # This file
```

### Configuration Files

- `docker-compose.yml`: Kafka broker configuration
- `requirements.txt`: Python package dependencies
- Environment variables can be set in `.env` file

### Useful Commands

```bash
# Stop all services
docker-compose down

# View resource usage
docker stats

# Clean up Docker
docker system prune -f

# Reset Python environment
pip freeze | xargs pip uninstall -y
pip install -r requirements.txt
```
