from __future__ import annotations

import logging

import pytest

from class_sorter.models.classes import Class
from class_sorter.models.sections import Section
from class_sorter.models.campers import Camper

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


@pytest.fixture
def valid_campers():
    return [
        {
            "first_name": "John",
            "last_name": "Doe",
            "cabin": "12",
            "age": 11,
            "allowed_to_shoot": True,
        },
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "cabin": "12",
            "age": 12,
            "allowed_to_shoot": False,
        },
        {
            "first_name": "Josh",
            "last_name": "Doe",
            "cabin": "12",
            "age": 12,
            "allowed_to_shoot": True,
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

    def test_get_available_sections(self, valid_classes):
        """
        Test that sections with room left are returned and are sorted
        from most room to least room.
        """

        class_ = Class(
            **valid_classes[2]
        )  # Class Capacity for section A is 0, so it should not be available

        class_sections = class_.get_available_sections()
        room_left = 10000
        for section in class_sections:
            assert isinstance(section, Section)

            capacity = section.get_remaining_capacity()
            assert capacity > 0
            assert capacity <= room_left
            room_left = capacity
            assert section.period != "A"

    def test_get_available_sections_empty_list(self, valid_classes):
        """
        Test that None is returned if there are no remaining classes
        """
        class_data = valid_classes[2].copy()
        # pretend all classes are full
        for period in class_data["period_capacities"]:
            class_data["period_capacities"][period] = 0
        class_ = Class(**class_data)

        assert class_.get_available_sections() == []

    def test_get_section(self, valid_classes):
        class_ = Class(**valid_classes[0])

        period = "A"
        section = class_.get_section(period)

        assert isinstance(section, Section)
        assert section.period == period

    def test_get_section_not_found_returns_none(self, valid_classes):
        class_ = Class(**valid_classes[0])

        section_id = "Z"  # An ID that doesn't exist

        assert class_.get_section(section_id) is None

    def test_can_enroll_blocks_enrollment(self, valid_classes, valid_campers):
        """
        Test that a camper is not enrolled when they do not meet age requirements,
        permissions requirements, or the class is full
        """
        class_data = valid_classes[0].copy()
        class_data["period_capacities"] = {
            "A": 0,
            "B": 0,
        }
        class_ = Class(
            **valid_classes[0]
        )  # age requirement is 12, shooting sports needed
        camper_1 = Camper(**valid_campers[0])
        camper_2 = Camper(**valid_campers[1])
        camper_3 = Camper(**valid_campers[2])
        class_2 = Class(**class_data)

        assert not class_.can_enroll(camper_1)
        assert not class_.can_enroll(camper_2)
        assert not class_2.can_enroll(camper_3)

    def test_can_enroll_allows_enrollment(self, valid_classes, valid_campers):
        """Test that can enroll returns true for an eligible camper"""

        class_ = Class(**valid_classes[0])
        camper = Camper(**valid_campers[2])

        assert class_.can_enroll(camper)

    def test_retrieve_optimal_section_returns_highest_capacity(
        self, valid_classes, valid_campers
    ):
        """
        Test that retrieve_optimal_section returns the section with the
        most remaining capacity among eligible sections.
        """
        # Class with uneven capacities: A=5, B=10, C=2
        class_data = {
            "class_id": "uneven",
            "period_capacities": {"A": 5, "B": 10, "C": 2},
            "minimum_age": 10,
            "shooting_permissions_needed": False,
        }
        class_ = Class(**class_data)
        camper = Camper(**valid_campers[2])  # Age 12, eligible

        optimal = class_.retrieve_optimal_section(camper)
        assert optimal is not None
        assert optimal.period == "B"

    def test_retrieve_optimal_section_skips_already_enrolled(
        self, valid_classes, valid_campers
    ):
        """
        Test that retrieve_optimal_section does not return a period
        the camper is already enrolled in.
        """
        class_data = {
            "class_id": "collision_test",
            "period_capacities": {"A": 10, "B": 10},
            "minimum_age": 10,
            "shooting_permissions_needed": False,
        }
        class_ = Class(**class_data)
        # Change class id so function will retrieve a valid section
        class_data['class_id'] = 'second_class'
        class_2 = Class(**class_data)
        camper = Camper(**valid_campers[2])

        # Manually enroll camper in period A
        section_a = class_.get_section("A")
        section_a.enroll_camper(camper)

        # Even though A has capacity, B should be the only choice
        optimal = class_2.retrieve_optimal_section(camper)
        assert optimal is not None
        assert optimal.period == "B"

    def test_retrieve_optimal_section_returns_none_when_full(
        self, valid_classes, valid_campers
    ):
        """
        Test that retrieve_optimal_section returns None if all eligible
        sections are at capacity.
        """
        class_data = {
            "class_id": "full_class",
            "period_capacities": {"A": 0, "B": 0},
            "minimum_age": 10,
            "shooting_permissions_needed": False,
        }
        class_ = Class(**class_data)
        camper = Camper(**valid_campers[2])

        assert class_.retrieve_optimal_section(camper) is None

    def test_retrieve_optimal_section_returns_none_for_ineligible_camper(
        self, valid_classes, valid_campers
    ):
        """
        Test that retrieve_optimal_section returns None if the camper
        fails the basic class requirements such as age or shooting permissions
        """
        class_ = Class(**valid_classes[0])  # min_age 12, shooting needed
        camper = Camper(**valid_campers[0])  # age 11, no shooting

        assert class_.retrieve_optimal_section(camper) is None
