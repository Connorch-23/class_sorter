import logging
from class_sorter.models.campers import Camper
from class_sorter.models.classes import Classes
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
    
        classes = [Classes(**class_data) for class_data in classes_raw]

        # Process
        # sorted_campers = sort_campers(campers, classes)

        # Export
        # export_results(sorted_campers, "outputs/sorted_campers.csv")

        print("Processing complete!")  # Results saved to outputs/sorted_campers.csv")

    except FileNotFoundError as e:
        print(f"Error: Required file not found - {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        
        ## TODO: Refactor test_data_loader.py for classes to adjust for new intake of period capacities
        ## TODO: Refactor data_loader.py for classes to adjust for new intake of period capacities such that all tests pass
        ## TODO: Create test_period.py to dictate the behavior periods        
        ## TODO: Create a class called Period. That period has the property class and capacity. Available periods are made from the classes list.
        ## TODO: Refactor class inputs to have a list of capacities for each period. This should either come as column1, column2, columnN or capacities= capacity;capacity;capacity where
        ## a blank cell means 0 capacity. 


if __name__ == "__main__":
    main()
