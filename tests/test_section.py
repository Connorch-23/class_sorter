import pytest
import logging
from class_sorter.models.sections import Section
from class_sorter.models.classes import Class
from class_sorter.models.campers import Camper

logger = logging.getLogger(__name__)


@pytest.fixture
def valid_camper():
    """A valid camper to be used and manipulated for testing"""
    return Camper({
        "first_name": "John",
        "last_name": "Doe",
        "cabin": "1",
        "age": 12,
        "allowed_to_shoot": True,
        "preferences": ["riflery", "climbing", "paintball"],
    })

@pytest.fixture
def valid_class():
    """A valid class to be used and manipulated for testing"""
    return Class(class_id="riflery", sections={"A": 15, "B": 15}, minimum_age=12, shooting_permissions_needed=True)

@pytest.fixture
def valid_sections(valid_class):
    """A set of valid sections to be used and manipulated for testing"""
    return [
        {
            "period": "A",
            "parent_class": valid_class,
            "capacity": 15,
        },
        {
            "period": "B",
            "parent_class": valid_class,
            "capacity": 15,
        }
    ]



class TestSectionInitialization:
    def test_section_object_populated(self, valid_sections, valid_class):
        """Testing a section can be created with an object"""
        parent_class = valid_class
        section_raw = valid_sections[0].copy()
        section_raw["parent_class"] = parent_class  # Ensure the parent_class is set correctly
        section = Section(**section_raw)

        assert section.period == section_raw["period"]
        assert section.capacity == section_raw["capacity"]
        assert section.parent_class == parent_class
        assert len(section.enrolled_campers) == 0

class TestSectionMethods:

    def test_enroll_camper(self, valid_sections, valid_camper):
        """Testing a camper can be enrolled in a section"""

        section = Section(**valid_sections[0])

        capacity = section.capacity

        camper = valid_camper

        # Enroll the camper
        section.enroll_camper(camper)

        # Check that the camper is enrolled
        assert len(section.enrolled_campers) == 1
        assert section.enrolled_campers[0] == camper
        assert section.capacity == capacity - 1 

    def test_enroll_camper_exceed_capacity(self, valid_sections, valid_camper):
        """Testing that enrolling a camper in a full section raises an error"""

        section = Section(**valid_sections[0])

        # Fill the section to capacity
        for _ in range(section.capacity):
            section.enroll_camper(valid_camper)

        # Now the section is full, trying to enroll another camper should raise an error
        with pytest.raises(ValueError) as excinfo:
            section.enroll_camper(valid_camper)

        assert "Section is full" in str(excinfo.value)