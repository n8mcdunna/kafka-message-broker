import json
import os
from time import time, sleep
from kafka import KafkaConsumer, KafkaProducer
from helpers import (
    process_message,
    should_publish_data,
    prepare_aggregated_data,
    reset_interval_data
)

# Environment variables from docker-compose.yml
BOOTSTRAP_SERVERS = os.environ.get('BOOTSTRAP_SERVERS')
CONSUMER_TOPIC = os.environ.get('KAFKA_TOPIC')
PROCESSED_TOPIC = 'user-login-processed'

# Set up Kafka consumer and producer
consumer = KafkaConsumer(
    CONSUMER_TOPIC,
    bootstrap_servers=[BOOTSTRAP_SERVERS],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=[BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Aggregation variables
last_publish_time = time()
interval_messages = 0
total_messages = 0
interval_device_type_count = {}
total_device_type_count = {}
interval_missing_field_count = {}
total_missing_field_count = {}

for message in consumer:
    print(f"Consumed message: {message}")
    data = message.value

    # Process and track data
    interval_messages += 1
    total_messages += 1
    process_message(
        data,
        interval_device_type_count,
        total_device_type_count, 
        interval_missing_field_count,
        total_missing_field_count
        )
    
    # Check if it's time to publish aggregated data
    current_time = time()
    if should_publish_data(current_time, last_publish_time):
        aggregated_data = prepare_aggregated_data(
            last_publish_time,
            current_time,
            interval_messages,
            total_messages, 
            interval_device_type_count,
            total_device_type_count, 
            interval_missing_field_count,
            total_missing_field_count
        )
        
        print(f"Sending aggregated data for last interval...")
        producer.send(PROCESSED_TOPIC, value=aggregated_data)
        print(f"Produced message: {aggregated_data}")
        
        # Small delay for readability in testing environments
        sleep(1)
        
        # Reset interval data and update publish time
        reset_interval_data(interval_device_type_count, interval_missing_field_count)
        interval_messages = 0
        last_publish_time = current_time


