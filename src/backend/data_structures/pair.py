from .person import Person
from .attribute import Attribute, Attributes
from typing import Dict, Optional


class Pair:
    """
    This class represents a pair of two people and calculates their compatibility scores
    based on their preferences and flexibility.
    """

    def __init__(self, person1: Person, person2: Person, attributes: Attributes):
        self.p1 = person1
        self.p2 = person2
        self.attributes = attributes  # Store a reference to the attributes object for future use

        # Store raw and adjusted selection scores
        self._selection_scores_raw: Dict[Attribute, float] = {}
        self._selection_scores: Dict[Attribute, float] = {}

        # Initialize raw and adjusted scores for active attributes
        self._initialize_scores()

    def _initialize_scores(self):
        """
        Initializes the raw and adjusted scores for all active attributes.
        """
        for attribute in self.attributes.get_active:
            raw_score = self._get_attribute_pcs_raw(attribute)
            adjusted_score = self._get_attribute_pcs(attribute, raw_score)

            # Update the dictionaries
            self._selection_scores_raw[attribute] = raw_score
            self._selection_scores[attribute] = adjusted_score

    def _get_attribute_pcs_raw(self, attribute: Attribute) -> float:
        """
        Calculates the raw compatibility score for an attribute based on the persons' selections.

        This method fetches the individual selections of the persons and uses the attribute's
        compatibility matrix to compute a compatibility score.

        Args:
            attribute (Attribute): The attribute for which to calculate the raw score.

        Returns:
            float: The raw compatibility score.
        """
        selection1 = self.p1.get_selection(attribute)
        selection2 = self.p2.get_selection(attribute)

        # Validate selections
        if selection1 is None or selection2 is None:
            raise ValueError(f"One or both persons do not have a valid selection for attribute '{attribute.name}'.")

        return attribute.get_selections_score(selection1, selection2)

    def _get_attribute_pcs(self, attribute: Attribute, raw_score: Optional[float] = None) -> float:
        """
        Adjusts the raw compatibility score for the attribute based on the flexibility scores of the two persons.

        The adjustment is made by considering the maximum flexibility between the two individuals.
        This allows more flexible individuals to contribute to a higher compatibility score.

        Args:
            attribute (Attribute): The attribute for which to adjust the score.
            raw_score (Optional[float]): The raw compatibility score. If not provided, it will be calculated.

        Returns:
            float: The adjusted compatibility score.
        """
        if raw_score is None:
            raw_score = self._get_attribute_pcs_raw(attribute)

        # Get flexibility scores, defaulting to 10 (fully flexible) if not defined
        p1_flexibility = self.p1.get_flexibility(attribute)
        p2_flexibility = self.p2.get_flexibility(attribute)

        # Ensure flexibility scores are valid
        if not (1 <= p1_flexibility <= 10):
            raise ValueError(f"Invalid flexibility score for person1: {p1_flexibility}")
        if not (1 <= p2_flexibility <= 10):
            raise ValueError(f"Invalid flexibility score for person2: {p2_flexibility}")

        # Adjust raw score using the maximum flexibility score
        adjusted_score = raw_score * (1 - (max(p1_flexibility, p2_flexibility) / 10))
        return adjusted_score

    @property
    def PCS_raw(self) -> float:
        """
        Computes and returns the weighted raw compatibility score across all active attributes.

        Returns:
            float: The total weighted raw compatibility score for this pair.
        """
        total_score = 0
        for attribute in self.attributes.get_active():
            total_score += self._selection_scores_raw[attribute] * attribute.get_weight()

        return total_score if total_score > 0 else 0.0

    @property
    def PCS(self) -> float:
        """
        Computes and returns the weighted adjusted compatibility score across all active attributes.

        Returns:
            float: The total weighted adjusted compatibility score for this pair.
        """
        total_score = 0
        for attribute in self.attributes.get_active:
            total_score += self._selection_scores[attribute] * attribute.get_weight()

        return total_score if total_score > 0 else 0.0

    @property
    def selection_scores_raw(self) -> Dict[Attribute, float]:
        """Returns a copy of the raw selection scores."""
        return self._selection_scores_raw.copy()

    @property
    def selection_scores(self) -> Dict[Attribute, float]:
        """Returns a copy of the adjusted selection scores."""
        return self._selection_scores.copy()