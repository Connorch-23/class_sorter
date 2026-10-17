import pytest
import logging
from class_sorter.models.campers import Camper
from class_sorter.models.classes import Class
logger = logging.getLogger(__name__)


@pytest.fixture
def valid_campers():
    """A set of valid campers to be used and manipulated for testing"""
    return [
        {
            "first_name": "Tyrese",
            "last_name": "Allen",
            "cabin": "11",
            "age": 12,
            "allowed_to_shoot": True,
            "preferences": [
                "riflery",
                "climbing",
                "paintball",
                "kayaking",
                "riflery",
                "12 stand",
            ],
        },
        {
            "first_name": "David",
            "last_name": "Atkins",
            "cabin": "11",
            "age": 13,
            "allowed_to_shoot": True,
            "preferences": [
                "paintball",
                "arts and crafts",
                "5 stand",
                "kayaking",
                "drama",
                "12 stand",
            ],
        },
        {
            "first_name": "Abigail",
            "last_name": "Bach",
            "cabin": "4",
            "age": 12,
            "allowed_to_shoot": True,
            "preferences": [
                "riflery",
                "drama",
                "5 stand",
                "kayaking",
                "photography",
                "12 stand",
            ],
        },
        {
            "first_name": "Elena ",
            "last_name": "Bishop",
            "cabin": "4",
            "age": 14,
            "allowed_to_shoot": False,
            "preferences": [
                "arts and crafts",
                "horses",
                "sports",
                "archery",
                "fishing",
                "12 stand",
            ],
        },
        {
            "first_name": "Julia",
            "last_name": "Brissie",
            "cabin": "4",
            "age": 12,
            "allowed_to_shoot": False,
            "preferences": [
                "horses",
                "sports",
                "drama",
                "arts and crafts",
                "kayaking",
                "12 stand",
            ],
        },
        {
            "first_name": "Danielle Mae",
            "last_name": "Casinillo",
            "cabin": "4L",
            "age": 15,
            "allowed_to_shoot": False,
            "preferences": [
                "archery",
                "newspaper",
                "arts and crafts",
                "sports",
                "5 stand",
                "12 stand",
            ],
        },
        {
            "first_name": "Paisley",
            "last_name": "Clarke",
            "cabin": "13",
            "age": 14,
            "allowed_to_shoot": False,
            "preferences": [
                "photography",
                "drama",
                "fishing",
                "sports",
                "arts and crafts",
                "12 stand",
            ],
        },
        {
            "first_name": "Miranda",
            "last_name": "Cole",
            "cabin": "4",
            "age": 13,
            "allowed_to_shoot": False,
            "preferences": [
                "drama",
                "archery",
                "newspaper",
                "fishing",
                "climbing",
                "12 stand",
            ],
        },
        {
            "first_name": "Jennifer",
            "last_name": "Crews",
            "cabin": "4L",
            "age": 12,
            "allowed_to_shoot": True,
            "preferences": [
                "riflery",
                "sports",
                "horses",
                "photography",
                "archery",
                "12 stand",
            ],
        },
        {
            "first_name": "Giulia",
            "last_name": "Duarte",
            "cabin": "13",
            "age": 13,
            "allowed_to_shoot": True,
            "preferences": [
                "drama",
                "fishing",
                "kayaking",
                "archery",
                "horses",
                "12 stand",
            ],
        },
    ]


class TestCamperInitialization:
    """Tests focused on how the Camper is constructed from input data"""

    # Happy path
    def test_camper_values_populated(self, valid_campers):
        """testing a camper can be created with individual named arguments"""
        camper_raw = valid_campers[1]
        camper = Camper(
            first_name=camper_raw["first_name"],
            last_name=camper_raw["last_name"],
            cabin=camper_raw["cabin"],
            age=camper_raw["age"],
            allowed_to_shoot=camper_raw["allowed_to_shoot"],
            preferences=camper_raw["preferences"]
        )

        assert camper.id > 0
        assert camper.first_name == camper_raw["first_name"]
        assert camper.last_name == camper_raw["last_name"]
        assert camper.cabin == camper_raw["cabin"]
        assert camper.age == camper_raw["age"]
        assert camper.allowed_to_shoot == camper_raw["allowed_to_shoot"]
        assert len(camper.preferences) == 6
        assert len(camper.classes) == 0

    def test_camper_object_populated(self, valid_campers):
        """Testing a camper can be created with an object"""
        camper_raw = valid_campers[1]
        camper = Camper(**camper_raw)

        assert camper.id > 0
        assert camper.first_name == camper_raw["first_name"]
        assert camper.last_name == camper_raw["last_name"]
        assert camper.cabin == camper_raw["cabin"]
        assert camper.age == camper_raw["age"]
        assert camper.allowed_to_shoot == camper_raw["allowed_to_shoot"]
        assert len(camper.preferences) == 6
        
    def test_unique_ids(self, valid_campers):
        """Test that every new camper gets a unique ID"""
        camper1 = Camper(**valid_campers[0])
        camper2 = Camper(**valid_campers[1])
        assert camper1.id != camper2.id
        
    def test_preferences_deque_working(self, valid_campers):
        """Checks that the preferences list is created as a deque for proper preference manipulation"""
        camper = Camper(**valid_campers[0].copy())
        
        assert camper.preferences.popleft() == valid_campers[0]["preferences"][0]
        
        
    # Edge Cases
    def test_preference_deduplication(self, valid_campers):
        """Test that duplicate preferences are handled (if your logic allows/requires it)"""
        # Tyrese has 'riflery' twice in the fixture
        camper_raw = valid_campers[0]
        camper = Camper(**camper_raw)
        # If your class is designed to deduplicate:
        assert len(camper.preferences) == 5
        assert set(camper.preferences) == set(camper_raw["preferences"])
        
    def test_empty_preferences_makes_empty_list(self, valid_campers):
        """Makes sure that empty preferences or preferences coming in as None gives an empty list"""
        row1 = valid_campers[0].copy()
        row2 = valid_campers[1].copy()
        
        row1['preferences'] = []
        row2['preferences'] = None
        
        camper1, camper2 = Camper(**row1), Camper(**row2)     
        
        assert len(camper1.preferences) == 0
        assert len(camper2.preferences) == 0
           

    def test_raises_error_on_missing_field(self, valid_campers):
        # Testing error handling during init
        raw_camper = valid_campers[0].copy()
        del raw_camper["first_name"]
        with pytest.raises(TypeError):
            Camper(**raw_camper)



        
class TestCamperMethods:
    """Tests focused on how camper properties/methods behave"""
    def test_get_enrolled_classes(self, valid_campers):
        camper = Camper(**valid_campers[0])
        enrolled_classes = camper.get_enrolled_classes()
        
        # Check that the result is a dictionary
        assert isinstance(enrolled_classes, dict)
        
        # Check that all expected keys are present
        expected_keys = {'A', 'B', 'C', 'D'}
        assert set(enrolled_classes.keys()) == expected_keys
        
        # Check that all values are instances of the Class model
        for class_obj in enrolled_classes.values():
            assert isinstance(class_obj, Class)