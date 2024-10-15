from src.backend.utils import read_csv, read_cfg


def main():
    # Load attributes from the configuration file
    attributes = read_cfg.load_attributes("../../resources/configuration/setup.json")

    # Load people from the CSV and activate optional attributes
    cohort = read_csv.create_cohort_from_csv("../../resources/input/v2_dummy_data.csv", attributes, nMax=5, nMin=3)

    # Allocate groups using the greedy algorithm
    cohort.allocate_groups_greedy()

    # Calculate and print cohort-level metrics
    mean_gcs = cohort.GCS_mean
    variance_gcs = cohort.GCS_variance

    print(f"Cohort created with {len(cohort.people)} people across {cohort.nGroups} groups.")
    print(f"Mean Group Compatibility Score (GCS) for the cohort: {mean_gcs if mean_gcs is not None else 'N/A'}")
    print(f"Variance of Group Compatibility Scores: {variance_gcs if variance_gcs is not None else 'N/A'}\n")

    # Print group-level metrics
    for i, group in enumerate(cohort.groups, 1):
        group_gcs = group.compute_GCS()
        group_variance = group.compute_PCS_variance()

        if group_gcs is None:
            print(f"Group {i}: GCS not computed.")
        else:
            most_compatible_pair = group.get_most_compatible_pair()
            least_compatible_pair = group.get_least_compatible_pair()

            print(f"Group {i}:")
            print(f"  Group Compatibility Score (GCS): {group_gcs:.2f}")
            print(f"  Variance of Pair Compatibility Scores: {group_variance:.2f}")
            print(f"  Most Compatible Pair: {most_compatible_pair.p1.name} & {most_compatible_pair.p2.name} (PCS: {most_compatible_pair.PCS():.2f})")
            print(f"  Least Compatible Pair: {least_compatible_pair.p1.name} & {least_compatible_pair.p2.name} (PCS: {least_compatible_pair.PCS():.2f})\n")

if __name__ == "__main__":
    main()