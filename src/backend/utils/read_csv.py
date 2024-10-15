import csv
from typing import List, Dict
from ..data_structures.person import Person
from ..data_structures.attribute import Attributes, Attribute
from ..data_structures.cohort import Cohort

def load_people_from_csv(file_path: str, attributes: Attributes) -> List[Person]:
    """
    Reads the CSV file and constructs a list of Person objects based on the attribute selections
    and flexibility provided in the CSV.
    """
    people = []

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row['name']
            sid = int(row['sid'])

            selections = {}
            flexibility_scores = {}

            # For each attribute, check if it's in the CSV
            for attribute in attributes.active:
                selection_column = attribute.name
                flexibility_column = f"{attribute.name} Flexibility"

                if selection_column in row:
                    # Add the selection and flexibility scores
                    selections[attribute] = row[selection_column]
                    if row[flexibility_column] != '':
                        flexibility_scores[attribute] = float(row[flexibility_column])
                    elif row[flexibility_column] == '':
                        flexibility_scores[attribute] = 0

            # Create a Person object
            person = Person(name, sid, selections=selections, flexibility_scores=flexibility_scores)
            people.append(person)



    return people


def activate_optional_attributes(attributes: Attributes, csv_data: List[Dict[str, str]]):
    """
    Checks the CSV data for any optional attributes that are present and activates them
    in the Attributes object by moving them from optional to active.
    """
    for attribute in attributes.options:
        if attribute.name in csv_data[0]:
            # Activate the attribute if it appears in the CSV
            attributes.active.append(attribute)


def create_cohort_from_csv(file_path: str, attributes: Attributes, nMax: int, nMin: int) -> Cohort:
    """
    Main function that reads the CSV, activates optional attributes found in the CSV,
    and returns a Cohort object.
    """
    # Load people from the CSV
    people = load_people_from_csv(file_path, attributes)

    # Activate any optional attributes present in the CSV
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        csv_data = list(reader)
        activate_optional_attributes(attributes, csv_data)

    # Return the cohort with the people and the updated attributes
    return Cohort(people, attributes, nMax=nMax, nMin=nMin)


# Example usage
if __name__ == "__main__":
    # Example of initializing attributes object (attributes should be loaded from config)
    attributes = Attributes(active=[], options=[])  # Assume this is properly loaded with Attribute objects

    # Load cohort from CSV
    cohort = create_cohort_from_csv('dummy_data_v2.csv', attributes, nMax=5, nMin=3)

    # Now the cohort is created with the people and pairs as per the CSV
    print(f"Cohort created with {len(cohort.people)} people.")
    print(f"Number of active attributes: {len(attributes.get_active)}")