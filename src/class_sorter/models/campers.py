from dataclasses import dataclass, field
from typing import ClassVar
from collections import deque

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

    def __post_init__(self):
        Camper._id_counter += 1
        self.id = Camper._id_counter
        if self.preferences is None:
            self.preferences = deque()
        else:
            self.preferences = deque(dict.fromkeys(self.preferences)) ## Use dict.fromkeys() instead of set() to remove duplicates while maintaining order.


        
