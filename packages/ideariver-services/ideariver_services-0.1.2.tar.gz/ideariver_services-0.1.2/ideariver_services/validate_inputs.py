def validate_inputs(metadata, input_data):
    """
    Validate input data based on the plugin's metadata.

    Args:
        metadata (dict): The plugin's metadata containing input specifications.
        input_data (dict): The actual input data provided to the plugin.

    Raises:
        ValueError: If any input data is invalid based on metadata specifications.
    """
    inputs_metadata = metadata.get("inputs", {})

    for input_name, input_spec in inputs_metadata.items():
        input_value = input_data.get(input_name, input_spec.get("default"))

        # Check if the input is required but not provided
        if input_spec.get("required") and input_value is None:
            raise ValueError(f"Input '{input_name}' is required but not provided.")

        # Check input type
        expected_type = input_spec.get("type")
        if expected_type == "number" and not isinstance(input_value, (int, float)):
            raise ValueError(f"Input '{input_name}' must be a number.")

        # Check range constraints (min, max)
        if "min" in input_spec and input_value < input_spec["min"]:
            raise ValueError(f"Input '{input_name}' is below the minimum value of {input_spec['min']}.")
        if "max" in input_spec and input_value > input_spec["max"]:
            raise ValueError(f"Input '{input_name}' exceeds the maximum value of {input_spec['max']}.")

    print("Input validation passed.")
