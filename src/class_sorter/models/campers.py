from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

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
    preferences: list[str] = field(default_factory=list, repr=False)
    
    # Internal state lists
    _preferences_stack: deque[str] = field(default_factory=deque, init=False)
    _enrolled_sections: dict[str, Section] = field(default_factory=dict, init=False)

    def __post_init__(self):
        Camper._id_counter += 1
        self.id = Camper._id_counter
        self.generate_preferences()
        
        
    def generate_preferences(self):
        """Generates preference list from raw preferences"""
        self._preferences_stack = deque(dict.fromkeys(self.preferences or [])) ## Use dict.fromkeys() instead of set() to remove duplicates while maintaining order.
        
    @property
    def enrolled_sections(self) -> dict[str, Section]:
        """Returns a dict copy of the camper's enrolled sections"""
        # wrapping in dict() creates a shallow copy of the sections dict. I think this should be read only.
        return dict(self._enrolled_sections)
    
    @property
    def preferences_stack(self) -> list[str]:
        """Returns the preferences as a list (live snapshot)."""
        # returning a list since this is a read only implementation of preferences
        return list(self._preferences_stack)

    def add_preference(self, preference: str):
        """Explicit method to add a preference, allowing for future validation."""
        if preference not in self._preferences_stack:
            self._preferences_stack.append(preference)

    def pop_preference(self) -> str | None:
        """
        Removes and returns the next preference from the front of the queue.
        Returns None if no preferences remain.
        """
        try:
            return self._preferences_stack.popleft()
        except IndexError:
            return None

    def add_section(self, section: Section):
        """Adds a section to the camper's list of enrolled sections."""
        self._enrolled_sections[section.period] = section
    
    def remove_section(self, section: Section):
        """Removes a section from the camper's enrolled sections"""
        if section.period not in self._enrolled_sections:
            raise ValueError(f"Camper {self.id} attempted to remove period {section.period} which was not found.")

        if self._enrolled_sections[section.period] != section:
            raise ValueError(f"Section integrity error: Period {section.period} exists but object mismatch.")

        self._enrolled_sections.pop(section.period)

        
