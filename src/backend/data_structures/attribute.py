from typing import List, Dict


class Attributes:
    def __init__(self, active: List[str], options: List[str]):
        # A list of all optional attributes from the attributes.yml.
        self.options = options

        # A list of all active attributes that are valid options.
        self.active = active

        # A list of all optional but inactive attributes.
        self.inactive = [a for a in options if a not in active]

    @property
    def get_active(self) -> List[str]:
        return self.active

    @property
    def get_inactive(self) -> List[str]:
        return self.inactive

    @property
    def get_options(self) -> List[str]:
        return self.options


class Attribute:
    def __init__(self, attribute_name: str, description: str, selections: List[str],
                 compatibility_matrix: Dict[str, Dict[str, float]], weight: float):
        # Input validation
        if not selections:
            raise ValueError("Selections list cannot be empty.")

        # Check compatibility matrix dimensions
        if len(compatibility_matrix) != len(selections) or any(
                len(compatibility_matrix[selection]) != len(selections) for selection in selections):
            raise ValueError(
                f"Compatibility matrix dimensions must match the number of selections for attribute '{attribute_name}'. "
                f"Selections: {len(selections)}, Matrix rows: {len(compatibility_matrix)}."
            )

        if not (0 <= weight <= 1):
            raise ValueError("Weight must be between 0 and 1.")

        # Initialize attributes
        self.name = attribute_name
        self.description = description
        self.selections = selections
        self.weight = weight

        # Keep the compatibility matrix as a dictionary
        self.compatibility_matrix = compatibility_matrix

        # Create a dictionary to map selections to their indices for quick access
        self.s_indices = {selection: i for i, selection in enumerate(selections)}

    def __str__(self):
        return f"Attribute(name={self.name}, description={self.description}, weight={self.weight})"

    def get_selections_score(self, s1: str, s2: str) -> float:
        """
        Get the compatibility score between two selections.

        Args:
            s1 (str): The first selection.
            s2 (str): The second selection.

        Returns:
            float: The compatibility score between the two selections.
        """
        if s1 not in self.compatibility_matrix or s2 not in self.compatibility_matrix[s1]:
            raise ValueError(f"Invalid selections: {s1} or {s2} not found in selections.")

        return self.compatibility_matrix[s1][s2]

    def get_weight(self) -> float:
        """
        Get the weight of the attribute.

        Returns:
            float: The weight of the attribute.
        """
        return self.weight