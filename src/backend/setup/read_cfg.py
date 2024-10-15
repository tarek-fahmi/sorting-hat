import logging
import yaml
from pathlib import Path
from typing import Dict, Optional
from src.backend.data_structures.attribute import Attributes, Attribute


def get_project_root() -> Path:
    """
    Get the absolute path to the root directory of the project (sorting-hat).
    """
    return Path(__file__).resolve().parent.parent.parent.parent


def load_yaml(file_path: Path) -> Dict:
    """
    Load YAML data from a file.

    Args:
        file_path (Path): The path to the YAML file.

    Returns:
        Dict: Parsed YAML data.
    """
    with file_path.open('r') as file:
        return yaml.safe_load(file)


def apply_custom_setting(custom_value: Optional[any], default_value: any) -> any:
    """
    Apply a custom setting if it exists, is not None, and is not the string 'None';
    otherwise, use the default value.

    Args:
        custom_value (Optional[any]): The custom value provided in config.yml.
        default_value (any): The default value specified in attributes.yml.

    Returns:
        any: The value to use (custom if provided and valid, otherwise default).
    """
    # Ensure that if the custom value is None or 'None', we use the default
    if custom_value is None or custom_value == 'None':
        return default_value
    return custom_value


def create_attribute_from_config(attr: Dict, custom_weights: Dict, custom_enabled: Dict) -> Attribute:
    """
    Create an Attribute object based on the defaults and custom settings.

    Args:
        attr (Dict): Attribute data from attributes.yml.
        custom_weights (Dict): Custom weight settings from config.yml.
        custom_enabled (Dict): Custom enabled/disabled settings from config.yml.

    Returns:
        Attribute: The created Attribute object.
    """
    # Extract default values from attributes.yml
    attribute_name = attr['name']
    description = attr['description']
    selections = attr['selections']

    # Construct compatibility matrix from attributes.yml, ensuring values are cast to floats
    compatibility_matrix = {
        selection1: {
            selection2: float(attr['compatibility_matrix'][selection1][selection2])
            for selection2 in selections
        }
        for selection1 in selections
    }

    # Default weight from attributes.yml
    default_weight = float(attr['default_weight'])  # Ensure it's treated as a float

    # Apply custom settings from config.yml if they exist
    custom_weight = apply_custom_setting(custom_weights.get(attribute_name), default_weight)

    # Ensure custom_weight is a valid float
    try:
        weight = float(custom_weight)
    except (ValueError, TypeError):
        logging.warning(f"Invalid custom weight for '{attribute_name}', falling back to default: {default_weight}")
        weight = default_weight

    # Apply custom enabled status, ensure it's boolean
    is_enabled = bool(apply_custom_setting(custom_enabled.get(attribute_name), attr['enabled_by_default']))

    # Log the applied values for better traceability
    logging.info(f"Attribute '{attribute_name}': Weight = {weight}, Enabled = {is_enabled}")

    # Create and return the Attribute object
    return Attribute(attribute_name, description, selections, compatibility_matrix, weight), is_enabled
def load_attributes(attributes_file: Path, config_file: Path) -> Attributes:
    """
    Load attributes from attributes.yml, apply custom settings from config.yml,
    and return an Attributes object with active and all options.

    Args:
        attributes_file (Path): The path to attributes.yml containing default attribute data.
        config_file (Path): The path to config.yml containing custom settings.

    Returns:
        Attributes: An instance of the Attributes class containing active and all options.
    """
    # Load default attributes and custom settings from YAML files
    attributes_data = load_yaml(attributes_file)
    config_data = load_yaml(config_file)

    # Get custom settings (handles missing fields by returning an empty dict if not found)
    custom_weights = config_data.get('custom_settings', {}).get('attributes', {}).get('weights', {})
    custom_enabled = config_data.get('custom_settings', {}).get('attributes', {}).get('enabled', {})

    # Initialize lists for active attributes and all options
    active_attributes = []
    all_options = []

    # Parse each attribute in attributes.yml
    for attr in attributes_data['attributes']:
        attribute_obj, is_enabled = create_attribute_from_config(attr, custom_weights, custom_enabled)

        # Add to active or optional attributes list based on enabled status
        if is_enabled:
            active_attributes.append(attribute_obj)
        all_options.append(attribute_obj)

    # Return the Attributes object containing active and all available attributes
    return Attributes(active=active_attributes, options=all_options)


def print_attributes(attributes: Attributes) -> None:
    """
    Nicely prints all attributes and their metadata.

    Args:
        attributes (Attributes): The Attributes object containing all options and active attributes.
    """

    print("\n--- All Attributes ---")
    for attr in attributes.options:
        status = "Active" if attr in attributes.active else "Inactive"
        print(f"Name: {attr.name} ({status})")
        is_active = "True"
        if attr not in attributes.active:
            is_active = "False"

        print(f"  Active:  {is_active}")
        print(f"  Description: {attr.description}")
        print(f"  Default Weight: {attr.weight}")
        print(f"  Selections: {', '.join(attr.selections)}")
        print("  Compatibility Matrix:")
        for selection, matrix in attr.compatibility_matrix.items():
            matrix_str = ', '.join([f"{key}: {value}" for key, value in matrix.items()])
            print(f"    {selection} -> {matrix_str}")
        print()


def main():
    # Set up logging

    # Get project root directory
    project_root = get_project_root()

    # Define the file paths relative to the project root
    attributes_file = project_root / 'configuration' / 'attributes.yml'
    config_file = project_root / 'configuration' / 'config.yml'

    # Load attributes
    attributes = load_attributes(attributes_file, config_file)

    # Print attributes and their metadata in a nice format
    print_attributes(attributes)


if __name__ == "__main__":
    main()