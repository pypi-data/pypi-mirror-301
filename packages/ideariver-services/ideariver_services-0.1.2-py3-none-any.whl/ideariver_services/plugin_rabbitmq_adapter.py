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
        Process the incoming RabbitMQ message, expecting an event-driven schema.
        """
        event = json.loads(body)
        
        # Extract event details
        event_id = event.get('event_id')
        event_type = event.get('event_type')
        source = event.get('source')
        timestamp = event.get('timestamp')
        payload = event.get('payload')  # This should contain plugin-specific data
        user_id = event.get('user_id')

        print(f"Processing event: {event_id}, type: {event_type}, from: {source}")

        # For PLUGIN_RUN event type, process the plugin
        if event_type == "PLUGIN_RUN":
            name_tag = payload.get('name_tag')
            plugin_payload = payload.get('payload')
            
            # Run the plugin using the plugin loader
            result = self.plugin_loader.run_plugin(name_tag, plugin_payload)
            print(f"Plugin result: {result}")
        
        # Acknowledge the message once processing is done
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



# class PluginRabbitMQAdapter:
#     def __init__(self, rabbitmq_url, queue_name, plugin_loader):
#         self.rabbitmq_url = rabbitmq_url
#         self.queue_name = queue_name
#         self.plugin_loader = plugin_loader

#         # Establish connection to RabbitMQ
#         self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
#         self.channel = self.connection.channel()

#         # Declare the queue
#         self.channel.queue_declare(queue=self.queue_name)

#     def process_message(self, ch, method, properties, body):
#         """
#         Process the incoming RabbitMQ message, run the plugin.
#         """
#         message = json.loads(body)
#         name_tag = message.get('name_tag')
#         payload = message.get('payload')

#         print(f"Processing message: {message}")

#         # Run the plugin using the plugin loader
#         result = self.plugin_loader.run_plugin(name_tag, payload)
#         print(f"Plugin result: {result}")

#         ch.basic_ack(delivery_tag=method.delivery_tag)

#     def start_consuming(self):
#         """
#         Start consuming messages from the queue.
#         """
#         self.channel.basic_consume(
#             queue=self.queue_name,
#             on_message_callback=self.process_message
#         )
#         print(f"Waiting for messages on queue '{self.queue_name}'...")
#         self.channel.start_consuming()
