from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from class_sorter.models.sections import Section
from class_sorter.models.campers import Camper

@dataclass
class Class:
    """
    Represents a course or activity that can be offered across multiple time periods.
    """
    class_id: str
    minimum_age: int
    # Dictionary mapping period {'A': 15, 'B': 7}
    period_capacities: dict[str, int]
    # The actual Section objects created from the capacities
    _sections: dict[str, Section] = field(default_factory=dict)
    shooting_permissions_needed: bool = False
    

    def __post_init__(self):
        """
        Initialize the sections based on the provided period_capacities.
        """
        for period, capacity in self.period_capacities.items():
            self._sections[period] = Section(
                period=period,
                parent_class_id=self.class_id,
                capacity=capacity
            )
            
    @property
    def sections(self) -> dict[Section]:
        """Returns a dictionary of all sections associated with this class"""
        return self._sections
            
    def get_section(self, period: str) -> Section | None:
        """Retrieves the section for a specific period."""
        return self._sections.get(period)
    
    def can_enroll(self, camper: Camper) -> bool:
        """
        Determines whether or not a camper is allowed to enroll in the class
        based on things like age or shooting permissions
        """

        if camper.age < self.minimum_age:
            return False
        if self.shooting_permissions_needed:
            return camper.allowed_to_shoot
        return any(section.get_remaining_capacity() > 0 for section in self._sections.values())


    def retrieve_optimal_section(self, camper: Camper) -> Section | None:
        """
        Determines the best section to be assigned to a camper based
        on their existing enrolled_sections
        """
        # look for periods not already filled (this might be removed for collision handling)
        available_periods = self._sections.keys() - camper.enrolled_sections
        
        if not available_periods:
            return None
        
        # retrieve actual sections
        available_sections = [self._sections[p] for p in available_periods]
        
        # sort available sections. Leaving as a sorted list for possible future implementation of return all possible sections
        available_sections = sorted(available_sections, key=lambda s: s.get_remaining_capacity(), reverse=True)
        
        return available_sections[0]
