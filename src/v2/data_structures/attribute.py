from typing import List


class Attributes:
    def __init__(self, active: List[str], options: List[str]):
        # A list of all optional attributes from the config.
        self.options = options

        # A list of all active attributes that are valid options.
        self.active = [a for a in active if a in options]

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
                 compatibility_matrix: List[List[float]], weight: float):
        # Input validation
        if not selections:
            raise ValueError("Selections list cannot be empty.")

        if len(compatibility_matrix) != len(selections) or any(
                len(row) != len(selections) for row in compatibility_matrix):
            raise ValueError("Compatibility matrix dimensions must match the number of selections.")

        if not (0 <= weight <= 1):
            raise ValueError("Weight must be between 0 and 1.")

        # Initialize attributes
        self.name = attribute_name
        self.description = description
        self.selections = selections
        self.weight = weight

        # Create a dictionary to map selections to their indices
        self.s_indices = {selection: i for i, selection in enumerate(selections)}

        # The 2D array storing the pre-determined Compatibility Score for each possible pair of selections
        self.cs_matrix = compatibility_matrix

    def __str__(self):
        return f"Attribute(name={self.name}, description={self.description}, weight={self.weight})"

    def get_selections_score(self, s1: str, s2: str) -> float:
        if s1 not in self.selections or s2 not in self.selections:
            raise ValueError(f"Invalid selections: {s1} or {s2} not found in selections.")

        return self.cs_matrix[self.s_indices[s1]][self.s_indices[s2]]