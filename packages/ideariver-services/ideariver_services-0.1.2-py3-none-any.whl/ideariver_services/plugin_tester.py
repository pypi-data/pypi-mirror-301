import json
import os
import pytest
import sys

# Path to the JSON file that contains plugin paths
PATHS_JSON_FILE = "plugin_paths.json"

# Function to load manifest.json and execute the tests
def load_and_execute_tests(plugin_path, original_dir):
    manifest_path = os.path.join(plugin_path, "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"No manifest found in {plugin_path}")
        return

    # Load the manifest.json
    with open(manifest_path, "r") as file:
        manifest = json.load(file)

    # Extract test information from the manifest
    test_info_list = manifest.get("test_info", [])
    if not test_info_list:
        print(f"No test info in manifest for {plugin_path}")
        return

    # Change directory to the plugin path
    os.chdir(plugin_path)

    # Add plugin_path to sys.path to ensure imports work
    sys.path.insert(0, plugin_path)

    # Loop through each test in the test_info array and run it
    for test_info in test_info_list:
        test_file = test_info.get("test_file")
        test_function = test_info.get("test_function")

        if test_file and test_function:
            print(f"Running test {test_function} in {test_file} for {manifest.get('title', 'Unknown Plugin')}...")

            # Run pytest on the test file and function
            if os.path.exists(test_file):
                print(f"Test file found: {test_file}")
                pytest.main([f"{test_file}::{test_function}"])
            else:
                print(f"Test file not found: {test_file}")
        else:
            print(f"Test info missing or incomplete for a test in {plugin_path}")

    # Change directory back to the original working directory after all tests
    os.chdir(original_dir)

# Function to read paths from a JSON file and test each plugin
def read_paths_and_test():
    # Ensure the paths file exists
    if not os.path.exists(PATHS_JSON_FILE):
        print(f"Paths file not found: {PATHS_JSON_FILE}")
        return

    # Load the paths from plugin_paths.json
    with open(PATHS_JSON_FILE, "r") as file:
        data = json.load(file)
        plugin_paths = data.get("plugin_paths", [])

        if not plugin_paths:
            print("No plugin paths found in the JSON file.")
            return

        # Store the original working directory to return to it after each test
        original_dir = os.getcwd()

        # Iterate over each plugin path and execute tests
        for plugin_path in plugin_paths:
            full_plugin_path = os.path.abspath(plugin_path)  # Get absolute path
            print(f"Checking path: {full_plugin_path}")
            if os.path.exists(full_plugin_path):
                # Switch to plugin directory and run the tests
                load_and_execute_tests(full_plugin_path, original_dir)
            else:
                print(f"Path does not exist: {plugin_path}")

if __name__ == "__main__":
    read_paths_and_test()
