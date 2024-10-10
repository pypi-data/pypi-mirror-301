import os
import pytest
from ideariver_services.plugin_loader import PluginLoader

@pytest.fixture(scope='module')
def plugin_loader():
    """
    Fixture to instantiate a real PluginLoader with the actual plugins directory.
    """
    return PluginLoader(plugins_folder='path_to_plugins_directory')  # Change the path accordingly

def test_add_and_run_plugin(plugin_loader):
    """
    Test that the plugin can be added, its directory is changed, and the plugin runs successfully.
    """
    plugin_metadata_file = 'plugins/sum/manifest.json'

    # Ensure the original directory is correct before loading the plugin
    original_dir = os.getcwd()

    # Add the plugin to the loader
    plugin_loader.add_plugin(plugin_metadata_file)

    # Ensure the directory is reset back to original
    assert os.getcwd() == original_dir, "Directory should be reset to the original after adding the plugin."

    # Define input data for the plugin
    input_data = {
        'a': 5,
        'b': 10
    }

    # Run the plugin and verify the result
    result = plugin_loader.run_plugin('sum_plugin', input_data)

    # Adjust the assertion to expect a dictionary
    assert result == {'sum': 15}, "The sum plugin did not return the expected result."

def test_list_plugins(plugin_loader):
    """
    Test that listing plugins shows the correct metadata.
    """
    plugin_metadata_file = 'plugins/sum/manifest.json'

    # Add the plugin to the loader
    plugin_loader.add_plugin(plugin_metadata_file)

    # List all loaded plugins and check for the correct metadata
    plugins = plugin_loader.list_plugins()

    # Check if the 'sum_plugin' exists in the list
    assert 'sum_plugin' in plugins, "Sum plugin should be listed after being added."

    # Check the relevant metadata fields of the sum plugin
    actual_metadata = plugins['sum_plugin']
    assert actual_metadata['nameTag'] == 'sum_plugin', "Name tag does not match."
    assert actual_metadata['executableFile'] == 'main.py', "Executable file does not match."  # Update this path to match the actual executable path

    # Optionally, you can add additional checks for other metadata fields if necessary
    assert 'author' in actual_metadata, "Author information should be present."
    assert 'version' in actual_metadata, "Version information should be present."
