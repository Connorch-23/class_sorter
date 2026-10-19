from dataclasses import dataclass, field
from typing import ClassVar
import logging
from src.class_sorter.models.classes import Class
from src.class_sorter.models.campers import Camper

logger = logging.getLogger(__name__)

@dataclass
class Section:
    """
    Respresents a single section in the system.
    Each section represents a class at a particular period
    """
    period: str
    parent_class: Class
    capacity: int
    enrolled_campers: list[Camper] = field(default_factory=list, init=False)