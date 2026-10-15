# from models.camper import Camper
# from models.class_ import Class
from class_sorter.services.data_loader import load_classes, load_campers
# from controllers.sorter import sort_campers
# from controllers.output_formatter import export_results


def main():
    """Main entry point for the campers/classes import system."""

    try:
        # Load data from CSV files
        classes_df = load_classes("inputs/classes_input.csv")
        campers_df = load_campers("inputs/Campers-test.csv")

        # Create objects
        # campers = [Camper(row) for _, row in campers_df.iterrows()]
        # classes = [Class(row) for _, row in classes_df.iterrows()]

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
