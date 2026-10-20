from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from class_sorter.models.campers import Camper

logger = logging.getLogger(__name__)

@dataclass
class Section:
    """
    Respresents a single section in the system.
    Each section represents a class at a particular period
    """
    period: str
    parent_class_id: str
    capacity: int
    _enrolled_campers: list[Camper] = field(default_factory=list, init=False, repr=False)
    
    @property
    def enrolled_campers(self) -> list[Camper]:
        """Returns a copy of the roster to prevent direct mutation of the internal state."""
        return list(self._enrolled_campers)
    
    def can_enroll(self, camper: Camper) -> bool:
        """Returns a boolean value to determine if there are spots left in the section."""
        return len(self._enrolled_campers) < self.capacity and not self.period in camper.enrolled_sections
    
    def enroll_camper(self, camper: Camper):
        """Adds the camper to the section's roster and adds the section to the camper's enrolled sections list"""
        if not self.can_enroll(camper): 
            return False
            
        # add to section roster
        self._enrolled_campers.append(camper)
        
        try:
            # Attempt to notify the camper
            camper.add_section(self)
            return True
        except Exception as e:
            self._enrolled_campers.remove(camper)
            logger.error(f"Failed to enroll camper due to internal error: {e}")
            return False
        
    def get_remaining_capacity(self) -> int:
        """Returns the remaining capacity of the section"""
        return self.capacity - len(self._enrolled_campers)
    
    def unenroll_camper(self, camper: Camper) -> bool:
        """
        Removes the camper from the section's roster and removes the section 
        from the camper's enrolled sections. Returns True if successful, 
        False if the camper wasn't enrolled.
        """        
        if camper not in self._enrolled_campers:
            logger.warning(f"Attempted to unenroll {camper.first_name} from {self.parent_class_id}, but they were not enrolled.")
            return False
        
        try:
            self._enrolled_campers.remove(camper)
            camper.remove_section(self)
            return True
        except (KeyError, ValueError) as e:
            logger.error(f"Critical state mismatch during unenrollment: {e}")
            # This handles the case where the camper's internal dict doesn't match the section's list.
            return False