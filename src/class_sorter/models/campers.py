from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar, TYPE_CHECKING
import logging
from collections import deque

if TYPE_CHECKING:
    from class_sorter.models.sections import Section
    
logger = logging.getLogger(__name__)

@dataclass
class Camper:
    """
    Represents a single camper in the system.
    """
    _id_counter: ClassVar[int] = 0
    id: int = field(init=False)

    first_name: str
    last_name: str
    cabin: str
    age: int
    allowed_to_shoot: bool
    preferences: deque[str] = field(default_factory=deque)
    _enrolled_sections: dict[str, Section] = field(default_factory=dict, init=False)

    def __post_init__(self):
        Camper._id_counter += 1
        self.id = Camper._id_counter
        if self.preferences is None:
            self.preferences = deque()
        else:
            self.preferences = deque(dict.fromkeys(self.preferences)) ## Use dict.fromkeys() instead of set() to remove duplicates while maintaining order.

    @property
    def enrolled_sections(self) -> dict[str, Section]:
        """Returns a dict of the camper's enrolled sections"""
        return dict(self._enrolled_sections)

    def add_section(self, section: Section):
        """Adds a section to the camper's list of enrolled sections."""
        self._enrolled_sections[section.period] = section
    
    def remove_section(self, section: Section):
        """Removes a section from the camper's enrolled sections"""
        if section.period not in self._enrolled_sections:
            logger.warning(f"Camper {self.id} attempted to remove period {section.period} which was not found.")
            return

        if self._enrolled_sections[section.period] != section:
            raise ValueError(f"Section integrity error: Period {section.period} exists but object mismatch.")

        self._enrolled_sections.pop(section.period)

        
