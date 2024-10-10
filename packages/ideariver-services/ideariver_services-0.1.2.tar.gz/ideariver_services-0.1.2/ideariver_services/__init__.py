# __init__.py

# Expose key components of the package

# Plugin Loader
from .plugin_loader import PluginLoader

# RabbitMQ Adapter
from .plugin_rabbitmq_adapter import PluginRabbitMQAdapter

# Input Validation (Utility)
from .validate_inputs import validate_inputs

# Plugin Testing
from .plugin_tester import read_paths_and_test, load_and_execute_tests

# Define the public API for the package (what should be accessible when importing)
__all__ = [
    'PluginLoader',
    'PluginRabbitMQAdapter',
    'validate_inputs',
    'read_paths_and_test',
    'load_and_execute_tests'
]