# utils/kafka_message_handler.py

"""
Kafka Message Handler

This module contains the KafkaMessageHandler class for processing Kafka messages.
"""

import json
from typing import Optional, Dict, Any
from loguru import logger


class KafkaMessageHandler:
    """
    Handles processing of Kafka messages including validation, deserialization, and metadata extraction.
    """
    
    def __init__(self):
        """Initialize the message handler."""
        pass
    
    def validate_message(self, msg) -> bool:
        """
        Validate that the message is not None and has no errors.
        
        Args:
            msg: Kafka message object
            
        Returns:
            bool: True if message is valid, False otherwise
        """
        if msg is None:
            logger.info("No message received, waiting...")
            return False
        
        if msg.error() is not None:
            logger.error(f"Error while consuming message: {msg.error()}")
            return False
        
        return True
    
    def handle_key(self, raw_key) -> Optional[str]:
        """
        Handle and decode message key.
        
        Args:
            raw_key: Raw key from Kafka message
            
        Returns:
            Optional[str]: Decoded key or None
        """
        if raw_key is not None and isinstance(raw_key, (bytes, bytearray)):
            try:
                return raw_key.decode("utf-8")
            except UnicodeDecodeError as e:
                logger.warning(f"Failed to decode message key: {e}")
                return None
        return raw_key
    
    def handle_value(self, raw_value, offset: int) -> Optional[Any]:
        """
        Handle and decode message value.
        
        Args:
            raw_value: Raw value from Kafka message
            offset: Message offset for logging
            
        Returns:
            Optional[Any]: Decoded and parsed value or None
        """
        logger.debug(f"Raw value: {raw_value}, type: {type(raw_value)}")
        
        if raw_value is None:
            logger.warning(f"Received message with NULL value at offset {offset}")
            return None
        
        if isinstance(raw_value, (bytes, bytearray)):
            try:
                decoded_value = raw_value.decode("utf-8")
                logger.debug(f"Decoded value: '{decoded_value}'")
                
                # Check if the decoded value is empty
                if not decoded_value.strip():
                    logger.warning(f"Received empty message at offset {offset}")
                    return None
                
                # Parse JSON
                return json.loads(decoded_value)
                
            except UnicodeDecodeError as e:
                logger.error(f"Failed to decode message at offset {offset}: {e}")
                return None
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON at offset {offset}: {e}")
                logger.error(f"Raw content: '{decoded_value}'")
                return None
        
        # raw_value is already a string or other type
        return raw_value
    
    def get_message_metadata(self, msg) -> Dict[str, Any]:
        """
        Extract metadata from the message.
        
        Args:
            msg: Kafka message object
            
        Returns:
            Dict[str, Any]: Message metadata
        """
        return {
            "offset": msg.offset(),
            "topic": msg.topic(),
            "partition": msg.partition(),
            "timestamp": msg.timestamp()[1] if msg.timestamp()[0] != -1 else None
        }
    
    def process_message(self, msg) -> Optional[Dict[str, Any]]:
        """
        Process a complete Kafka message.
        
        Args:
            msg: Kafka message object
            
        Returns:
            Optional[Dict[str, Any]]: Processed message data or None if processing failed
        """
        # Validate message
        if not self.validate_message(msg):
            return None
        
        try:
            # Handle key
            key = self.handle_key(msg.key())
            
            # Handle value
            value = self.handle_value(msg.value(), msg.offset())
            
            # Skip if value processing failed
            if value is None and msg.value() is not None:
                return None
            
            # Get metadata
            metadata = self.get_message_metadata(msg)
            
            # Combine all data
            return {
                "key": key,
                "value": value,
                **metadata
            }
            
        except Exception as e:
            logger.error(f"Unexpected error processing message at offset {msg.offset()}: {e}")
            logger.error(f"Message details: key={msg.key()}, value={msg.value()}")
            return None
    
    def log_processed_message(self, processed_data: Dict[str, Any]) -> None:
        """
        Log the processed message data.
        
        Args:
            processed_data: Processed message data dictionary
        """
        key = processed_data.get("key")
        value = processed_data.get("value")
        offset = processed_data.get("offset")
        topic = processed_data.get("topic")
        partition = processed_data.get("partition")
        timestamp = processed_data.get("timestamp")
        
        logger.success(f"""
Message processed successfully at timestamp: {timestamp}
Topic: {topic}, Partition: {partition}, Offset: {offset}
Key: {key} (type: {type(key)})
Value: {value} (type: {type(value)})
                    """)

class TopicAwareMessageHandler(KafkaMessageHandler):
    """
    Extended message handler that can use QuixStreams topic for deserialization.
    """
    
    def __init__(self, topic=None):
        """
        Initialize with optional topic for enhanced deserialization.
        
        Args:
            topic: QuixStreams topic object
        """
        super().__init__()
        self.topic = topic
    
    def handle_value_with_topic(self, msg) -> Optional[Any]:
        """
        Handle value using topic deserializer with fallback to manual processing.
        
        Args:
            msg: Kafka message object
            
        Returns:
            Optional[Any]: Deserialized value or None
        """
        if self.topic:
            try:
                # Try topic-based deserialization
                deserialized_msg = self.topic.deserialize(msg)
                # logger.debug(f"Deserialized message object: {type(deserialized_msg)}")
                
                # Extract the actual value from the KafkaMessage object
                if hasattr(deserialized_msg, 'value'):
                    value = deserialized_msg.value
                    # logger.debug(f"Extracted value from deserialized message: {value}, type: {type(value)}")
                    return value
                else:
                    # If it's not a KafkaMessage object, return it directly
                    logger.debug(f"Direct deserialized value: {deserialized_msg}, type: {type(deserialized_msg)}")
                    return deserialized_msg
                    
            except Exception as e:
                logger.warning(f"Topic deserialization failed: {e}, falling back to manual processing")
        
        # Fallback to manual processing
        return self.handle_value(msg.value(), msg.offset())
    
    def process_message(self, msg) -> Optional[Dict[str, Any]]:
        """
        Process message with topic-aware deserialization.
        
        Args:
            msg: Kafka message object
            
        Returns:
            Optional[Dict[str, Any]]: Processed message data or None if processing failed
        """
        # Validate message
        if not self.validate_message(msg):
            return None
        
        try:
            # Handle key
            key = self.handle_key(msg.key())
            
            # Handle value with topic support
            value = self.handle_value_with_topic(msg)
            
            # Skip if value processing failed
            if value is None and msg.value() is not None:
                return None
            
            # Get metadata
            metadata = self.get_message_metadata(msg)
            
            # Combine all data
            return {
                "key": key,
                "value": value,
                **metadata
            }
            
        except Exception as e:
            logger.error(f"Unexpected error processing message at offset {msg.offset()}: {e}")
            logger.error(f"Message details: key={msg.key()}, value={msg.value()}")
            return None
