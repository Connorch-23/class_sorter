from __future__ import annotations
import pytest
import logging
from class_sorter.models.classes import Class
from class_sorter.models.sections import Section
logger = logging.getLogger(__name__)


@pytest.fixture
def valid_classes():
    """A set of valid classes to be used and manipulated for testing"""
    return [
        {
            "class_id": "riflery",
            "period_capacities": {
                "A": 15,
                "B": 15,
                "C": 15,
                "D": 15,
            },
            "minimum_age": 12,
            "shooting_permissions_needed": True,
        },
        {
            "class_id": "drama",
            "period_capacities": {
                "A": 15,
                "B": 15,
                "C": 15,
                "D": 15,
            },
            "minimum_age": None,
            "shooting_permissions_needed": False,
        },
        {
            "class_id": "five_stand",
            "period_capacities": {
                "A": 0,
                "B": 1,
                "C": 15,
                "D": 14,
            },
            "minimum_age": 14,
            "shooting_permissions_needed": True,
        },
        {
            "class_id": "paintball",
            "period_capacities": {
                "A": 10,
                "B": 10,
                "C": 10,
                "D": 0,
            },
            "minimum_age": 12,
            "shooting_permissions_needed": True,
        },
    ]


class TestClassInitialization:
    """Tests focused on how the class is constructed from input data"""

    def test_class_values_populated(self, valid_classes):
        """testing a class can be created with individual named arguments"""

        class_raw = valid_classes[0]

        class_ = Class(
            class_id=class_raw["class_id"],
            period_capacities=class_raw["period_capacities"],
            minimum_age=class_raw["minimum_age"],
            shooting_permissions_needed=class_raw["shooting_permissions_needed"],
        )

        assert class_.class_id == class_raw["class_id"]
        assert class_.minimum_age == class_raw["minimum_age"]
        assert (
            class_.shooting_permissions_needed
            == class_raw["shooting_permissions_needed"]
        )
        assert class_.period_capacities.keys() == class_raw["period_capacities"].keys()

    def test_class_object_populated(self, valid_classes):
        """Testing a class can be created with an object"""
        class_raw = valid_classes[1]
        class_ = Class(**class_raw)

        assert class_.class_id == class_raw["class_id"]
        assert class_.minimum_age == class_raw["minimum_age"]
        assert (
            class_.shooting_permissions_needed
            == class_raw["shooting_permissions_needed"]
        )


class TestClassMethods:
    """Tests focused on how class properties/methods behave"""

    def test_get_sections(self, valid_classes):
        class_ = Class(**valid_classes[0])

        rosters = class_.sections

        assert isinstance(rosters, dict)  
        for section_id, section in rosters.items():
            assert isinstance(section_id, str)
            assert isinstance(section, Section) 

    # def test_get_available_sections(self, valid_classes):
    #     class_ = Class(**valid_classes[2]) # Class Capacity for section A is 0, so it should not be available

    #     class_sections = class_.get_available_sections()

    #     assert isinstance(class_sections, list)
    #     assert len(class_sections) == 3  # Only sections B, C, and D should be available

    def test_get_section(self, valid_classes):
        class_ = Class(**valid_classes[0])

        period = "A"
        section = class_.get_section(period)

        assert isinstance(section, Section)
        assert section.period == period


    # def test_get_available_sections_empty(self, valid_classes):
    #     class_data = valid_classes[3].copy()
    #     # Set all section capacities to 0
    #     for section in class_data["sections"]:
    #         class_data["sections"][section] = 0
    #     class_ = Class(class_data)  # All sections have capacity 0

    #     class_sections = class_.get_available_sections()

    #     assert isinstance(class_sections, dict)
    #     assert len(class_sections) == 0  # No sections should be available

    
    def test_get_section_not_found_returns_none(self, valid_classes):
        class_ = Class(**valid_classes[0])

        section_id = "Z"  # An ID that doesn't exist
        
        assert class_.get_section(section_id) is None
