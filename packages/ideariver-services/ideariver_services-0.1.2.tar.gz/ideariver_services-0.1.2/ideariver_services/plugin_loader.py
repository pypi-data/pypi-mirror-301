import importlib.util
import json
import os
from ideariver_services.validate_inputs import validate_inputs

class PluginLoader:
    def __init__(self, plugins_folder):
        self.plugins_folder = plugins_folder
        self.plugins = {}

    def load_metadata(self, metadata_file):
        """
        Load plugin metadata from a JSON file.
        """
        with open(metadata_file, 'r') as f:
            return json.load(f)

    def add_plugin(self, metadata_file):
        """
        Add a plugin to the system by loading its metadata and executable.
        """
        metadata = self.load_metadata(metadata_file)
        name_tag = metadata['nameTag']

        # Temporarily change to the plugin directory
        original_dir = os.getcwd()
        plugin_dir = os.path.dirname(metadata_file)

        try:
            os.chdir(plugin_dir)
            
            # Load the plugin's executable file dynamically
            spec = importlib.util.spec_from_file_location(name_tag, metadata['executableFile'])
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)

            # Manually reference the class name directly, assuming it is SumPlugin
            plugin_class = getattr(plugin_module, "SumPlugin")

            # Instantiate the plugin class
            plugin_instance = plugin_class()

            # Store plugin metadata and instance
            self.plugins[name_tag] = {
                'metadata': metadata,
                'instance': plugin_instance
            }
        finally:
            # Reset back to the original directory
            os.chdir(original_dir)

    def load_plugins_from_paths(self):
        """
        Load all plugins listed in the plugin_paths.json file.
        """
        with open(self.plugins_folder, 'r') as f:
            paths_data = json.load(f)

        # Iterate through each path in the JSON file and load the plugin
        for plugin_path in paths_data.get("plugin_paths", []):
            manifest_file = os.path.join(plugin_path, 'manifest.json')
            if os.path.exists(manifest_file):
                self.add_plugin(manifest_file)

    def remove_plugin(self, name_tag):
        """
        Remove a plugin by its nameTag.
        """
        if name_tag in self.plugins:
            del self.plugins[name_tag]
        else:
            raise ValueError(f"No plugin found with nameTag '{name_tag}'")

    def init_plugin(self, name_tag, services):
        """
        Initialize the plugin by passing utility services.
        """
        if name_tag not in self.plugins:
            raise ValueError(f"No plugin found with nameTag '{name_tag}'")

        # Initialize the plugin with services
        plugin_instance = self.plugins[name_tag]['instance']
        plugin_instance.init(services)

    def run_plugin(self, name_tag, input_data):
        """
        Execute the run method of a plugin, with input validation.
        """
        if name_tag not in self.plugins:
            raise ValueError(f"No plugin found with nameTag '{name_tag}'")

        # Get plugin metadata and validate inputs
        plugin_metadata = self.plugins[name_tag]['metadata']
        validate_inputs(plugin_metadata, input_data)

        # Execute the run method of the plugin
        plugin_instance = self.plugins[name_tag]['instance']
        return plugin_instance.run(input_data)

    def list_plugins(self):
        """
        List all loaded plugins and their metadata.
        """
        return {tag: plugin['metadata'] for tag, plugin in self.plugins.items()}



# import importlib.util
# import json
# import os
# from validate_inputs import validate_inputs

# class PluginLoader:
#     def __init__(self, plugins_folder):
#         self.plugins_folder = plugins_folder
#         self.plugins = {}

#     def load_metadata(self, metadata_file):
#         """
#         Load plugin metadata from a JSON file.
#         """
#         with open(metadata_file, 'r') as f:
#             return json.load(f)

#     def add_plugin(self, metadata_file):
#         """
#         Add a plugin to the system by loading its metadata and executable.
#         """
#         metadata = self.load_metadata(metadata_file)
#         name_tag = metadata['nameTag']

#         # Temporarily change to the plugin directory
#         original_dir = os.getcwd()
#         plugin_dir = os.path.dirname(metadata_file)

#         try:
#             os.chdir(plugin_dir)
            
#             # Load the plugin's executable file dynamically
#             spec = importlib.util.spec_from_file_location(name_tag, metadata['executableFile'])
#             plugin_module = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(plugin_module)

#             # Manually reference the class name directly, assuming it is SumPlugin
#             plugin_class = getattr(plugin_module, "SumPlugin")

#             # Instantiate the plugin class
#             plugin_instance = plugin_class()

#             # Store plugin metadata and instance
#             self.plugins[name_tag] = {
#                 'metadata': metadata,
#                 'instance': plugin_instance
#             }
#         finally:
#             # Reset back to the original directory
#             os.chdir(original_dir)

#     def remove_plugin(self, name_tag):
#         """
#         Remove a plugin by its nameTag.
#         """
#         if name_tag in self.plugins:
#             del self.plugins[name_tag]
#         else:
#             raise ValueError(f"No plugin found with nameTag '{name_tag}'")

#     def init_plugin(self, name_tag, services):
#         """
#         Initialize the plugin by passing utility services.
#         """
#         if name_tag not in self.plugins:
#             raise ValueError(f"No plugin found with nameTag '{name_tag}'")

#         # Initialize the plugin with services
#         plugin_instance = self.plugins[name_tag]['instance']
#         plugin_instance.init(services)

#     def run_plugin(self, name_tag, input_data):
#         """
#         Execute the run method of a plugin, with input validation.
#         """
#         if name_tag not in self.plugins:
#             raise ValueError(f"No plugin found with nameTag '{name_tag}'")

#         # Get plugin metadata and validate inputs
#         plugin_metadata = self.plugins[name_tag]['metadata']
#         validate_inputs(plugin_metadata, input_data)

#         # Execute the run method of the plugin
#         plugin_instance = self.plugins[name_tag]['instance']
#         return plugin_instance.run(input_data)

#     def list_plugins(self):
#         """
#         List all loaded plugins and their metadata.
#         """
#         return {tag: plugin['metadata'] for tag, plugin in self.plugins.items()}
