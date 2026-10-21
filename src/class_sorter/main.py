import logging
import pandas as pd

from class_sorter.models.campers import Camper
from class_sorter.models.classes import Class
from class_sorter.services.assignment import AssignmentEngine
from class_sorter.services.data_loader import load_campers, load_classes

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
        
        engine.assign_greedy(10)
        
        for c in classes[:1]:
            for section in c.sections.values():
                print(section)
                print(section.enrolled_campers)


        rows = []
        for camper in campers:
            score = 0.0
            for section in camper.enrolled_sections.values():
                if section.parent_class_id in camper.preferences:
                    # Rank 0 (1st choice) -> score 1.0
                    # Rank 1 (2nd choice) -> score 0.5
                    # Rank 2 (3rd choice) -> score 0.33
                    rank_index = camper.preferences.index(section.parent_class_id)
                    score += 1.0 / (rank_index + 1)
                else:
                    # No preference match adds nothing to the score
                    score += 0.0

            rows.append({
                'id': camper.id,
                'last_name': camper.last_name,
                'first_name': camper.first_name,
                'cabin': camper.cabin,
                **{period: section.parent_class_id for period, section in sorted(camper.enrolled_sections.items())},
                'score': round(score, 2)
            })
        # Create DataFrame and export
        df = pd.DataFrame(rows)
        
        # Ensure columns are in a predictable order if possible, 
        # but since periods are dynamic, we'll just write it.
        output_path = "outputs/sorted_campers.csv"
        df.to_csv(output_path, index=False)

        print("Processing complete!")  # Results saved to outputs/sorted_campers.csv")

    except FileNotFoundError as e:
        print(f"Error: Required file not found - {e}")
    except Exception as e:  # noqa: BLE001
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
