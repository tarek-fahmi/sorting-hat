from person import Person
from pair import Pair
from attribute import Attributes
from group import Group
from typing import List, Dict, Tuple
import random
import math

class Cohort:
    def __init__(self, people: List[Person], attributes: Attributes, nMax: int, nMin: int):
        # List of people in the cohort.
        self._people = people
        self.size = len(people)

        # Attributes and pair dictionary
        self._attributes = attributes
        self._pairs = self._load_pairs(people)

        # Group settings
        self.nMax = nMax
        self.nMin = nMin
        self._groups = []
        self._nGroups = 0

        # Group compatibility metrics
        self._GCS_mean = 0
        self._GCS_variance = 0

    def _load_pairs(self, people: List[Person]) -> Dict[Tuple[Person, Person], Pair]:
        '''
        Initializes the dictionary of pairs for the cohort.
        '''
        people_dict = {}

        for i, p1 in enumerate(people):
            for p2 in people[i + 1:]:
                if (p1, p2) not in people_dict and (p2, p1) not in people_dict:
                    people_dict[(p1, p2)] = Pair(p1, p2, self._attributes)

        return people_dict

    def find_pair(self, p1: Person, p2: Person) -> Pair:
        '''
        Finds and returns the pair object for the given persons, creating a new pair if necessary.
        '''
        if (p1, p2) in self._pairs:
            return self._pairs[(p1, p2)]
        elif (p2, p1) in self._pairs:
            return self._pairs[(p2, p1)]

        # Create a new pair if it doesn't exist
        new_pair = Pair(p1, p2, self._attributes)
        self._pairs[(p1, p2)] = new_pair
        return new_pair

    def allocate_groups_greedy(self):
        '''
        Allocates groups using a greedy approach, aiming to maximize initial group compatibility.
        '''
        # Sort pairs by compatibility score in descending order
        sorted_pairs = sorted(self._pairs.values(), key=lambda pair: pair.PCS, reverse=True)

        # Create groups and assign pairs to groups
        self._groups = []
        unassigned_people = set(self._people)

        # Create initial empty groups
        while len(self._groups) * self.nMin < len(self._people):
            self._groups.append(Group(self))

        # Add people to groups based on highest compatibility
        for pair in sorted_pairs:
            if pair.p1 in unassigned_people and pair.p2 in unassigned_people:
                # Find a group that can accommodate both members
                for group in self._groups:
                    if group.size + 2 <= self.nMax:
                        group.add_pair(pair)
                        unassigned_people.discard(pair.p1)
                        unassigned_people.discard(pair.p2)
                        break

        # Add any remaining unassigned people to the groups
        for person in unassigned_people:
            # Find the group with the smallest size that can add this person
            smallest_group = min(self._groups, key=lambda g: g.size)
            if smallest_group.size < self.nMax:
                smallest_group.add_member(person)

        # Update group count and GCS variance
        self._nGroups = len(self._groups)
        self.compute_GCS_variance()

    def allocate_groups_SA(self):
        '''
        Allocates groups using Simulated Annealing to optimize group compatibility scores.
        '''
        # Initial greedy allocation
        self.allocate_groups_greedy()

        # Parameters for simulated annealing
        temperature = 100
        cooling_rate = 0.95
        min_temperature = 0.01

        def get_total_variance():
            return self.compute_GCS_variance()

        current_variance = get_total_variance()

        while temperature > min_temperature:
            # Randomly select two groups and swap a random member between them
            group1, group2 = random.sample(self._groups, 2)
            if group1.size > 0 and group2.size > 0:
                person1 = random.choice(group1.members)
                person2 = random.choice(group2.members)

                # Swap members
                group1.remove_member(person1)
                group2.remove_member(person2)
                group1.add_member(person2)
                group2.add_member(person1)

                # Calculate new variance
                new_variance = get_total_variance()

                # Decide whether to accept the swap
                if new_variance < current_variance:
                    current_variance = new_variance
                else:
                    # Revert swap with a probability depending on temperature
                    if math.exp((current_variance - new_variance) / temperature) < random.random():
                        # Revert swap
                        group1.remove_member(person2)
                        group2.remove_member(person1)
                        group1.add_member(person1)
                        group2.add_member(person2)
                    else:
                        current_variance = new_variance

            # Cool down the temperature
            temperature *= cooling_rate

        # Update mean and variance after optimization
        self._GCS_mean = sum(group.GCS for group in self._groups) / self._nGroups
        self._GCS_variance = get_total_variance()

    def compute_GCS_variance(self) -> float:
        '''
        Calculates the variance of the Group Compatibility Scores (GCS) across all groups in the cohort.
        '''
        if self._nGroups < 2:
            self._GCS_variance = 0
            return 0

        gcs_scores = [group.GCS for group in self._groups]
        mean_gcs = sum(gcs_scores) / len(gcs_scores)
        variance = sum((gcs - mean_gcs) ** 2 for gcs in gcs_scores) / len(gcs_scores)

        self._GCS_variance = variance
        return variance

    @property
    def people(self) -> List[Person]:
        '''Returns a list of people in the cohort.'''
        return self._people.copy()

    @property
    def pairs(self) -> Dict[Tuple[Person, Person], Pair]:
        '''Returns the dictionary of pairs in the cohort.'''
        return self._pairs.copy()

    @property
    def groups(self) -> List[Group]:
        '''Returns the list of groups in the cohort.'''
        return self._groups.copy()

    @property
    def GCS_mean(self) -> float:
        '''Returns the mean group compatibility score.'''
        return self._GCS_mean

    @property
    def GCS_variance(self) -> float:
        '''Returns the variance of group compatibility scores.'''
        return self._GCS_variance

    @property
    def nGroups(self) -> int:
        '''Returns the number of groups in the cohort.'''
        return self._nGroups