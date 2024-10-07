from person import Person
from pair import Pair
from typing import List, Optional
from math import inf


class Group:
    '''
    This class represents a group of people and handles the computation of compatibility scores
    for the group as a whole.
    '''

    def __init__(self, cohort, members: Optional[List[Person]] = None):
        self.members = members if members else []  # List of `Person` instances in the group
        self.min_size = cohort.nMin  # Minimum number of members allowed in the group
        self.max_size = cohort.nMax  # Maximum number of members allowed in the group
        self.cohort = cohort

        # Compatibility scores and group metrics
        self._pcs_dict = {}  # Dictionary to store pairwise compatibility scores
        self._GCS = 0  # Overall compatibility score of the group
        self._PCS_variance = 0

        # Compute the initial group compatibility score if members are present
        if self.members:
            self.compute_GCS()

    def add_member(self, person: Person):
        '''
        Adds a new member to the group and updates the group's compatibility scores.
        '''
        if len(self.members) >= self.max_size:
            raise ValueError("Cannot add member: Group has reached its maximum size.")
        if person in self.members:
            raise ValueError(f"{person.name} is already a member of this group.")

        # Add the new member
        self.members.append(person)

        # Recompute the GCS and variance
        self.compute_GCS()
        self.compute_PCS_variance()

    def add_pair(self, pair: Pair):
        '''
        Adds a pair of persons to the group if they are not already assigned to a group.
        '''
        if pair.p1.group is None:
            self.add_member(pair.p1)
            pair.p1.group = self  # Update person's group assignment
        else:
            print(f"{pair.p1.sid} is already allocated in a group.")

        if pair.p2.group is None:
            self.add_member(pair.p2)
            pair.p2.group = self  # Update person's group assignment
        else:
            print(f"{pair.p2.sid} is already allocated in a group.")

    def remove_member(self, person: Person):
        '''
        Removes a member from the group and updates the group's compatibility scores.
        '''
        if person not in self.members:
            raise ValueError(f"{person.name} is not a member of this group.")

        # Remove the member
        self.members.remove(person)

        # Recompute the GCS and variance
        self.compute_GCS()
        self.compute_PCS_variance()

    def compute_GCS(self):
        '''
        Computes the overall compatibility score of the group by averaging the pairwise scores.
        '''
        if len(self.members) < 2:
            self._GCS = 0
            return

        total_score = 0
        num_pairs = 0

        for i, p1 in enumerate(self.members):
            for p2 in self.members[i + 1:]:
                pair_key = (p1, p2) if (p1, p2) in self.cohort.pairs else (p2, p1)
                pair_current = self.cohort.pairs.get(pair_key)
                if pair_current:
                    total_score += pair_current.PCS
                    num_pairs += 1

        self._GCS = total_score / num_pairs if num_pairs > 0 else 0

    @property
    def GCS(self) -> float:
        '''Returns the overall group compatibility score.'''
        return self._GCS

    def compute_PCS_variance(self):
        '''
        Calculates the variance of pairwise compatibility scores within the group.
        '''
        if len(self.members) < 2:
            self._PCS_variance = 0
            return

        scores = []
        for i, p1 in enumerate(self.members):
            for p2 in self.members[i + 1:]:
                pair_key = (p1, p2) if (p1, p2) in self.cohort.pairs else (p2, p1)
                pair_current = self.cohort.pairs.get(pair_key)
                if pair_current:
                    scores.append(pair_current.PCS)

        mean_score = sum(scores) / len(scores) if scores else 0
        self._PCS_variance = sum((x - mean_score) ** 2 for x in scores) / len(scores) if scores else 0

    @property
    def PCS_variance(self) -> float:
        '''Returns the variance of pairwise compatibility scores.'''
        return self._PCS_variance

    def get_most_compatible_pair(self) -> Optional[Pair]:
        '''
        Identifies and returns the most compatible pair in the group based on pairwise scores.
        '''
        if len(self.members) < 2:
            return None

        max_pair = None
        max_score = -inf

        for i, p1 in enumerate(self.members):
            for p2 in self.members[i + 1:]:
                pair_key = (p1, p2) if (p1, p2) in self.cohort.pairs else (p2, p1)
                pair_current = self.cohort.pairs.get(pair_key)
                if pair_current and pair_current.PCS > max_score:
                    max_score = pair_current.PCS
                    max_pair = pair_current

        return max_pair

    def get_least_compatible_pair(self) -> Optional[Pair]:
        '''
        Identifies and returns the least compatible pair in the group based on pairwise scores.
        '''
        if len(self.members) < 2:
            return None

        min_pair = None
        min_score = inf

        for i, p1 in enumerate(self.members):
            for p2 in self.members[i + 1:]:
                pair_key = (p1, p2) if (p1, p2) in self.cohort.pairs else (p2, p1)
                pair_current = self.cohort.pairs.get(pair_key)
                if pair_current and pair_current.PCS < min_score:
                    min_score = pair_current.PCS
                    min_pair = pair_current

        return min_pair

    @property
    def size(self) -> int:
        '''Returns the current size of the group.'''
        return len(self.members)

    @property
    def all_members(self) -> List[Person]:
        '''Returns a copy of the members in the group.'''
        return self.members.copy()