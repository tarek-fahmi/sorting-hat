import json
from typing import List, Dict
from data_structures.attribute import Attributes, Attribute


def load_attributes(file_path: str) -> Attributes:
    # Load the JSON data from the file
    with open(file_path, 'r') as f:
        config_data = json.load(f)

    # Initialize lists for active attributes and all available options
    active_attributes = []
    all_options = []

    # Loop through each attribute in the config
    for attr in config_data['attributes']:
        # Extract necessary data
        attribute_name = attr['name']
        description = attr['description']
        selections = attr['selections']
        compatibility_matrix = [[float(score) for score in row.values()] for row in
                                attr['compatibility_matrix'].values()]
        weight = attr['default_weight']
        enabled_by_default = attr['enabled_by_default']

        # Create an Attribute object
        attribute_obj = Attribute(attribute_name, description, selections, compatibility_matrix, weight)

        # Add the attribute name to the options list
        all_options.append(attribute_name)

        # Add to active attributes if it's enabled by default
        if enabled_by_default:
            active_attributes.append(attribute_name)

    # Return an Attributes object containing active and optional attributes
    return Attributes(active=active_attributes, options=all_options)


def apply_customizations(attribute_objects: List[Attribute], customization_file: str) -> None:
    # Load the customization data
    with open(customization_file, 'r') as f:
        customizations = json.load(f)['customizations']

    # Create a dictionary for quick lookup of customizations by attribute name
    customizations_dict = {c['name']: c for c in customizations}

    # Apply customizations to attribute objects
    for attribute in attribute_objects:
        if attribute.name in customizations_dict:
            customization = customizations_dict[attribute.name]
            attribute.enabled = customization['enabled']
            attribute.weight = customization['weight']

# Example usage
if __name__ == '__main__':
    # Assuming 'config.json' contains the attributes JSON structure
    config_path = './resources/cfg_default.json'

    # Load the attributes
    attributes = load_attributes(config_path)
    apply_customizations(attributes.options, 'customization.json')

    # Accessing active and inactive attributes
    print("Active Attributes:", attributes.get_active)
    print("Inactive Attributes:", attributes.get_inactive)
    print("All Options:", attributes.get_options)