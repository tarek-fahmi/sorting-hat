import json
from typing import List, Dict
from src.backend.data_structures.attribute import Attributes, Attribute


def load_attributes(file_path: str) -> Attributes:
    """
    Load attributes from a JSON file, parse them, and return an Attributes object.

    Args:
        file_path (str): The path to the JSON file containing attribute data.

    Returns:
        Attributes: An instance of the Attributes class containing active and all options.
    """
    # Load the JSON data from the file
    with open(file_path, 'r') as f:
        config_data = json.load(f)

    # Initialize lists for active attributes and all available options
    active_attributes = []
    all_options = []

    # Loop through each attribute in the setup.json
    for attr in config_data['attributes']:
        # Extract necessary data
        attribute_name = attr['name']
        description = attr['description']
        selections = attr['selections']

        # Create compatibility matrix (leave it as a 2D dictionary)
        compatibility_matrix = {
            selection1: {
                selection2: float(attr['compatibility_matrix'][selection1][selection2])
                for selection2 in selections
            }
            for selection1 in selections
        }

        weight = attr['default_weight']

        # Create an Attribute object
        attribute_obj = Attribute(attribute_name, description, selections, compatibility_matrix, weight)

        # Add the attribute name to the options list
        all_options.append(attribute_obj)

    # Return an Attributes object containing active and optional attributes
    return Attributes(active=active_attributes, options=all_options)