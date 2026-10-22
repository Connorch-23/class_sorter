import logging

from class_sorter.models.campers import Camper
from class_sorter.models.classes import Class
from class_sorter.services.assignment import AssignmentEngine
from class_sorter.services.data_loader import load_campers, load_classes
from class_sorter.services.output_data import output_rosters

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the campers/classes import system."""

    try:
        # Load data from CSV files
        classes_raw = load_classes("inputs/classes_input.csv")
        campers_raw = load_campers("inputs/campers_input.csv")
        print(f"Camper csv loaded {len(campers_raw)} dictionaries")

        # Create objects
        campers = [Camper(**camper_data) for camper_data in campers_raw]
        print(f"Loaded {len(campers)} Camper objects")

        classes = [Class(**class_data) for class_data in classes_raw]
        print(f"Loaded {len(classes)} Class objects")

        # Process campers into classes
        engine = AssignmentEngine(campers, classes)

        scores = []
        times_to_run = 50
        for seed in range(times_to_run):
            scores.append(engine.assign_greedy(seed))
            engine.reset()
        print(f"Scores: {scores}")
        print(f"Max score occured on run {scores.index(max(scores)) + 1} / {times_to_run}: {max(scores)}")

        engine.assign_greedy(scores.index(max(scores)))

        output_path = "outputs/sorted_campers.csv"

        output_rosters(path=output_path, campers=campers, classes=classes)

        print("Processing complete!")  # Results saved to outputs/sorted_campers.csv")
        print("Saved to outputs/sorted_campers.csv")

    except FileNotFoundError as e:
        print(f"Error: Required file not found - {e}")
    except Exception as e:  # noqa: BLE001
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
