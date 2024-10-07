from typing import Optional, Dict
from attribute import Attribute

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

        self.group = None  # To be assigned when the person is added to a group

        # Flexibility scores for each attribute; uses an integer (1-10 scale)
        self.flexibility_scores = flexibility_scores if flexibility_scores else {}

    def __str__(self):
        return f"Person(name={self.name}, sid={self.sid})"

    def get_flexibility(self, attribute: Attribute) -> int:
        """
        Retrieves the flexibility score for a given attribute. Returns a default score if not set.
        """
        return self.flexibility_scores.get(attribute, 10)

    def get_selection(self, attribute: Attribute) -> Optional[str]:
        """
        Retrieves the selected option for a given attribute. Returns None if not set.
        """
        return self.selections.get(attribute)

    def update_selection(self, attribute: Attribute, selection: str):
        """
        Updates the selected option for a given attribute. Ensures the selection is valid.
        """
        if selection not in attribute.selections:
            raise ValueError(f"Invalid selection '{selection}' for attribute '{attribute.name}'.")

        if attribute not in self.selections:
            print(f"Adding new selection for {attribute.name}.")

        self.selections[attribute] = selection

    def update_flexibility(self, attribute: Attribute, score: int):
        """
        Updates the flexibility score for a given attribute. Score must be between 1 and 10.
        """
        if not 1 <= score <= 10:
            raise ValueError(f"Flexibility score must be between 1 and 10. Received: {score}")
        self.flexibility_scores[attribute] = score

    @property
    def all_selections(self) -> Dict[Attribute, str]:
        """Returns a copy of all selections."""
        return self.selections.copy()

    @property
    def all_flexibility_scores(self) -> Dict[Attribute, int]:
        """Returns a copy of all flexibility scores."""
        return self.flexibility_scores.copy()