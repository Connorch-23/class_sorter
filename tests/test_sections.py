import logging

import pytest

from class_sorter.models.campers import Camper
from class_sorter.models.sections import Section

logger = logging.getLogger(__name__)


@pytest.fixture
def valid_camper(first_name="John", last_name="Doe"):
    """A valid camper to be used and manipulated for testing"""
    return Camper(
        first_name=first_name,
        last_name=last_name,
        cabin="1",
        age=12,
        allowed_to_shoot=True,
        preferences=["riflery", "climbing", "paintball"],
    )


@pytest.fixture
def valid_sections():
    """A set of valid sections to be used and manipulated for testing"""
    return [
        {
            "period": "A",
            "parent_class_id": "riflery",
            "capacity": 15,
        },
        {
            "period": "B",
            "parent_class_id": "riflery",
            "capacity": 0,
        },
        {
            "period": "C",
            "parent_class_id": "riflery",
            "capacity": 1,
        },
    ]


class TestSectionInitialization:
    def test_section_object_populated(self, valid_sections):
        """Testing a section can be created with an object"""
        section_raw = valid_sections[0].copy()
        section = Section(**section_raw)

        assert section.period == section_raw["period"]
        assert section.capacity == section_raw["capacity"]
        assert section.parent_class_id == section_raw["parent_class_id"]
        assert len(section.enrolled_campers) == 0


class TestSectionMethods:
    def test_can_enroll_when_capacity_available(self, valid_sections, valid_camper):
        """Testing that can_enroll returns True when there is space"""
        # Using index 0 which has capacity 15
        section = Section(**valid_sections[0])
        assert section.can_enroll(valid_camper) is True

    def test_can_enroll_when_at_capacity(self, valid_sections, valid_camper):
        """Testing that can_enroll returns False when capacity is 0"""
        # Using index 1 which has capacity 0
        section = Section(**valid_sections[1])
        assert section.can_enroll(valid_camper) is False

    def test_enroll_camper(self, valid_sections, valid_camper):
        """Testing a camper can be enrolled in a section"""

        section = Section(**valid_sections[0])

        camper = valid_camper

        # Enroll the camper
        section.enroll_camper(camper)

        # Check that the camper is enrolled
        assert len(section.enrolled_campers) == 1
        assert section.enrolled_campers[0] == camper
        assert section in camper.enrolled_sections.values()
        assert len(camper.enrolled_sections) == 1

    def test_enroll_camper_exceed_capacity(self, valid_sections, valid_camper):
        """Testing that enrolling a camper in a full section raises an error"""

        section = Section(**valid_sections[2]) # capcity for section[2] is 1
        # Fill the section to capacity
        section.enroll_camper(valid_camper)
            
        second_camper = Camper(first_name="Jane", last_name="Doe", cabin="1", age=12, allowed_to_shoot=True)

        # Now the section is full, trying to enroll another camper should return False
        assert not section.enroll_camper(second_camper)
        assert len(section.enrolled_campers) == 1
        assert section.get_remaining_capacity() == section.capacity - 1
        assert section not in second_camper.enrolled_sections.values()
        assert len(second_camper.enrolled_sections) == 0


    def test_enroll_multiple_different_campers(self, valid_sections, valid_camper):
        """Testing that multiple different campers can be enrolled sequentially"""
        section = Section(**valid_sections[0])
        second_camper = Camper(first_name="Jane", last_name="Doe", cabin="1", age=12, allowed_to_shoot=True)


        section.enroll_camper(valid_camper)
        section.enroll_camper(second_camper)

        assert len(section.enrolled_campers) == 2
        assert section.get_remaining_capacity() == valid_sections[0]["capacity"] - 2

    def test_enroll_same_camper_twice_returns_false(self, valid_sections, valid_camper):
        """Testing that enrolling the same camper twice in the same section raises an error"""
        section = Section(**valid_sections[0])

        # First enrollment should succeed
        section.enroll_camper(valid_camper)

        # Second enrollment of the same camper should raise an error
        assert not section.enroll_camper(valid_camper)
    
    def test_get_remaining_capacity(self, valid_sections, valid_camper):
        """Tests if enrolling a camper reduces the remaining capacity"""
        
        section = Section(**valid_sections[0])
        
        section.enroll_camper(valid_camper)
        
        assert section.get_remaining_capacity() == section.capacity - 1

    def test_unenroll_camper(self, valid_sections, valid_camper):
        """Testing that a camper can be unenrolled and capacity is restored"""
        section = Section(**valid_sections[0])

        # Setup: Enroll a camper
        section.enroll_camper(valid_camper)
        assert len(section.enrolled_campers) == 1
        assert section.get_remaining_capacity() == section.capacity - 1

        # Action: Unenroll
        section.unenroll_camper(valid_camper)

        # Assertions
        assert len(section.enrolled_campers) == 0
        assert section.get_remaining_capacity() == section.capacity
        assert section not in valid_camper.enrolled_sections.values()