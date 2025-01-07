import json
import pika


def publish_followup_notification(followup_data):
    """Publish the follow-up notification to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='followup_notifications')  # Declare the queue

    # Prepare the message
    message = {
        'user_email': followup_data['user_email'],
        'jobId': followup_data['jobId'],
        'status': followup_data['status'],
        'notes': followup_data.get('notes'),
        'nextStep': followup_data.get('nextStep'),
        'followUpDate': followup_data.get('followUpDate'),
    }

    # Publish the message
    channel.basic_publish(exchange='',
                          routing_key='followup_notifications',
                          body=json.dumps(message))

    connection.close()

