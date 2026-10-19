from dataclasses import dataclass, field
from typing import ClassVar
from class_sorter.models.sections import Section

@dataclass
class Class:
    """
    Represents a single class in the system.
    """
    class_id: str
    minimum_age: int = None
    shooting_permissions_needed: bool = False
    sections: dict[Section]

    # def __post_init__(self):
    #     self.sections = {
    #         key: Section(**value) if isinstance(value, dict) else value 
    #         for key, value in self.sections.items()
    #     }