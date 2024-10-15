from typing import Optional, Dict
from .attribute import Attribute

class Person:
    """
    This class represents a student with a name, SID, and various selections (preferences).
    It also supports interactions with group assignments and flexibility scores.
    """

    def __init__(self, name: str, sid: int,
                 selections: Optional[Dict[Attribute, str]] = None,
                 flexibility_scores: Optional[Dict[Attribute, int]] = None):
        self.name = name
        self.sid = sid

        # A dictionary with Attribute keys and selected options as values
        self.selections = selections if selections else {}

        # To store the group assignment when the person is added to a group
        self.group = None

        # Flexibility scores for each attribute; uses an integer (1-10 scale)
        self.flexibility_scores = flexibility_scores if flexibility_scores else {}

    def __str__(self):
        return f"Person(name={self.name}, sid={self.sid})"

    def get_flexibility(self, attribute: Attribute) -> int:
        """
        Retrieves the flexibility score for a given attribute. Returns a default score (10) if not set.

        Args:
            attribute (Attribute): The attribute for which the flexibility score is requested.

        Returns:
            int: The flexibility score, defaulting to 10 if not set.
        """
        return self.flexibility_scores.get(attribute, 10)

    def get_selection(self, attribute: Attribute) -> Optional[str]:
        """
        Retrieves the selected option for a given attribute. Returns None if not set.

        Args:
            attribute (Attribute): The attribute for which the selection is requested.

        Returns:
            Optional[str]: The selected option for the attribute, or None if not set.
        """
        return self.selections.get(attribute)

    def update_selection(self, attribute: Attribute, selection: str):
        """
        Updates the selected option for a given attribute. Ensures the selection is valid.

        Args:
            attribute (Attribute): The attribute to update.
            selection (str): The new selection for the attribute.

        Raises:
            ValueError: If the selection is not a valid option for the attribute.
        """
        if selection not in attribute.selections:
            raise ValueError(f"Invalid selection '{selection}' for attribute '{attribute.name}'.")

        # Add or update the selection
        if attribute not in self.selections:
            print(f"Adding new selection for {attribute.name}.")

        self.selections[attribute] = selection

    def update_flexibility(self, attribute: Attribute, score: int):
        """
        Updates the flexibility score for a given attribute. Score must be between 1 and 10.

        Args:
            attribute (Attribute): The attribute to update.
            score (int): The new flexibility score for the attribute.

        Raises:
            ValueError: If the score is not between 1 and 10.
        """
        if not 1 <= score <= 10:
            raise ValueError(f"Flexibility score must be between 1 and 10. Received: {score}")

        # Update the flexibility score
        self.flexibility_scores[attribute] = score

    @property
    def all_selections(self) -> Dict[Attribute, str]:
        """
        Returns a copy of all selections.

        Returns:
            Dict[Attribute, str]: A dictionary of all selected options.
        """
        return self.selections.copy()

    @property
    def all_flexibility_scores(self) -> Dict[Attribute, int]:
        """
        Returns a copy of all flexibility scores.

        Returns:
            Dict[Attribute, int]: A dictionary of all flexibility scores.
        """
        return self.flexibility_scores.copy()