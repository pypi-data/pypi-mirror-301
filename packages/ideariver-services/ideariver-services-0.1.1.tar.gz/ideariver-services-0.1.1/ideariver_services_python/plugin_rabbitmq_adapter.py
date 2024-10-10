import pika
import json

class PluginRabbitMQAdapter:
    def __init__(self, rabbitmq_url, queue_name, plugin_loader):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.plugin_loader = plugin_loader

        # Establish connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        self.channel = self.connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue=self.queue_name)

    def process_message(self, ch, method, properties, body):
        """
        Process the incoming RabbitMQ message, run the plugin.
        """
        message = json.loads(body)
        name_tag = message.get('name_tag')
        payload = message.get('payload')

        print(f"Processing message: {message}")

        # Run the plugin using the plugin loader
        result = self.plugin_loader.run_plugin(name_tag, payload)
        print(f"Plugin result: {result}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        """
        Start consuming messages from the queue.
        """
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message
        )
        print(f"Waiting for messages on queue '{self.queue_name}'...")
        self.channel.start_consuming()
