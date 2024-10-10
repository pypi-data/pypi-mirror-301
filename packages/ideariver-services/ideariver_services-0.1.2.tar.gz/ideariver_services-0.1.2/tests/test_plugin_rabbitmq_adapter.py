import pytest
import pika
import json
from ideariver_services.plugin_rabbitmq_adapter import PluginRabbitMQAdapter
from ideariver_services.plugin_loader import PluginLoader

@pytest.fixture(scope='module')
def rabbitmq_connection():
    """
    Setup RabbitMQ connection and queue.
    """
    connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@localhost:5672/'))
    channel = connection.channel()
    queue_name = 'test_plugin_queue'
    channel.queue_declare(queue=queue_name)
    yield connection, channel, queue_name
    channel.queue_delete(queue=queue_name)
    connection.close()

@pytest.fixture(scope='module')
def plugin_loader():
    """
    Initialize PluginLoader by reading the plugin_paths.json and loading the plugins listed.
    """
    loader = PluginLoader(plugins_folder='plugin_paths.json')  # Points to the JSON file with plugin paths
    
    # Load all plugins from plugin_paths.json
    loader.load_plugins_from_paths()
    
    return loader

@pytest.fixture
def adapter(plugin_loader, rabbitmq_connection):
    """
    Initialize RabbitMQ adapter with the plugin loader.
    """
    connection, channel, queue_name = rabbitmq_connection
    return PluginRabbitMQAdapter(
        rabbitmq_url='amqp://guest:guest@localhost:5672/',
        queue_name=queue_name,
        plugin_loader=plugin_loader
    )

def send_message(channel, queue_name, message):
    """
    Helper to send a message to RabbitMQ queue.
    """
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))

def test_process_message(rabbitmq_connection, adapter):
    """
    Test processing a message by sending data to RabbitMQ, which should trigger sum_plugin.
    """
    connection, channel, queue_name = rabbitmq_connection
    
    # Example event-driven message
    event_message = {
        'event_id': 'event-001',
        'event_type': 'PLUGIN_RUN',
        'source': 'plugin-service',
        'timestamp': '2024-10-09T12:34:56Z',
        'payload': {
            'name_tag': 'sum_plugin',
            'payload': {'a': 5, 'b': 10}
        },
        'user_id': '12345'
    }

    send_message(channel, queue_name, event_message)

    method_frame, header_frame, body = channel.basic_get(queue_name)
    if body:
        adapter.process_message(channel, method_frame, header_frame, body)

def test_message_acknowledgement(rabbitmq_connection, adapter):
    """
    Test that RabbitMQ messages are acknowledged after the plugin processes them.
    """
    connection, channel, queue_name = rabbitmq_connection
    message = {'name_tag': 'sum_plugin', 'payload': {'a': 3, 'b': 4}, 'user_id': '67890'}
    send_message(channel, queue_name, message)

    method_frame, header_frame, body = channel.basic_get(queue_name)
    if body:
        adapter.process_message(channel, method_frame, header_frame, body)

    # Removed manual channel.basic_ack as the adapter already handles the acknowledgment
