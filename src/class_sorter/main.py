import logging
from class_sorter.models.campers import Camper
from class_sorter.models.classes import Class
from class_sorter.services.data_loader import load_classes, load_campers
# from controllers.sorter import sort_campers
# from controllers.output_formatter import export_results

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

        # Process
        # sorted_campers = sort_campers(campers, classes)

        # Export
        # export_results(sorted_campers, "outputs/sorted_campers.csv")

        print("Processing complete!")  # Results saved to outputs/sorted_campers.csv")

    except FileNotFoundError as e:
        print(f"Error: Required file not found - {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        


if __name__ == "__main__":
    main()
