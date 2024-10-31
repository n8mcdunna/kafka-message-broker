# Helper functions for streaming data pipeline

# Fields expected in consumer topic messages
CONSUMER_TOPIC_FIELDS = ['user_id', 'app_version', 'ip', 'locale', 'device_id', 'timestamp', 'device_type']
AGGREGATION_INTERVAL_SECONDS = 10

def process_message(
        data,
        interval_device_type_count,
        total_device_type_count, 
        interval_missing_field_count,
        total_missing_field_count
    ):
    """
    Processes the incoming message, tracks missing fields, and counts device types.
    """
    for field in CONSUMER_TOPIC_FIELDS:
        if field not in data:
            interval_missing_field_count[field] = interval_missing_field_count.get(field, 0) + 1
            total_missing_field_count[field] = total_missing_field_count.get(field, 0) + 1

    device_type = data.get('device_type')
    if device_type:
        interval_device_type_count[device_type] = interval_device_type_count.get(device_type, 0) + 1
        total_device_type_count[device_type] = total_device_type_count.get(device_type, 0) + 1

def should_publish_data(current_time, last_publish_time):
    """
    Checks if enough time has passed to publish the aggregated data.
    """
    return (current_time - last_publish_time) > AGGREGATION_INTERVAL_SECONDS

def prepare_aggregated_data(
        last_publish_time,
        current_time,
        interval_messages_consumed,
        total_messages_consumed, 
        interval_device_type_count,
        total_device_type_count, 
        interval_missing_field_count,
        total_missing_field_count
    ):
    """
    Prepares the aggregated data to be sent to the processed topic.
    """
    return {
        "timestamp_start": int(last_publish_time),
        "timestamp_end": int(current_time),
        "interval_messages_consumed": interval_messages_consumed,
        "total_messages_consumed": total_messages_consumed,
        "interval_missing_field_count": dict(interval_missing_field_count),
        "interval_device_type_count": dict(interval_device_type_count),
        "total_missing_field_count": dict(total_missing_field_count),
        "total_device_type_count": dict(total_device_type_count)
    }

def reset_interval_data(interval_device_type_count, interval_missing_field_count):
    """
    Resets interval-specific data after publishing.
    """
    interval_device_type_count.clear()
    interval_missing_field_count.clear()
