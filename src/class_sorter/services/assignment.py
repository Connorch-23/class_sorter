import random

from class_sorter.models.campers import Camper
from class_sorter.models.classes import Class


class AssignmentEngine:
    def __init__(
        self,
        campers: list[Camper],
        classes: list[Class],
    ):
        self.campers = campers
        self.classes = {c.class_id: c for c in classes}
        self.num_classes_to_assign = len(
            {period for c in classes for period in c.period_capacities}
        )

        # Internal State
        self.rng = None
        
    def assign_greedy(self, seed) -> float:
        # set seed at the top of the run
        self.rng = random.Random(seed)

        # create a shallow copy of the campers to not affect original camper order
        randomized_campers = self.campers.copy()
        self.rng.shuffle(randomized_campers)

        # Loop until all campers have the correct number of classes
        while any(
            len(c.enrolled_sections) < self.num_classes_to_assign
            for c in randomized_campers
        ):
            progress = False

            # Iterate through campers' preferences one preference at a time
            for camper in randomized_campers:
                # If they already have a full schedule, move on
                if len(camper.enrolled_sections) >= self.num_classes_to_assign:
                    continue

                preference = camper.pop_preference()

                # If we've processed all their preferences, add a the class with the most room left that can take them
                if preference is None:
                    max_capacity = 0
                    for c in self.classes.values():
                        section = c.retrieve_optimal_section(camper)
                        if (
                            section is not None
                            and section.get_remaining_capacity() > max_capacity
                        ):
                            max_capacity = section.get_remaining_capacity()
                            preference = section.parent_class_id


                class_ = self.classes.get(preference)

                # Perform some checks on the class and section they've requested, moving on if they can't be added to that preference
                if class_ is None:
                    continue
                if not class_.can_enroll(camper):
                    continue
                section = class_.retrieve_optimal_section(camper)
                if section is None:
                    continue
                if section.enroll_camper(camper):
                    progress = True

            # progress checks if we kids are still getting assigned to classes, progress is only changed on successful enrollment
            if not progress:
                break

        return sum(round(c.score, 2) for c in self.campers)

    def reset(self):
        """Function built to reset campers and classes back to original state."""
        for class_ in self.classes.values():
            for section in class_.sections.values():
                for camper in section.enrolled_campers.copy():
                    section.unenroll_camper(camper)

        for camper in self.campers:
            camper.generate_preferences()
