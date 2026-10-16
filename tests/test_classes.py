import pytest
import logging
from class_sorter.models.classes import Class

logger = logging.getLogger(__name__)


@pytest.fixture
def valid_classes():
    """A set of valid classes to be used and manipulated for testing"""
    return [
        {
            "class_id": "riflery",
            "capacity_a": 15,
            "capacity_b": 15,
            "capacity_c": 15,
            "capacity_d": 15,
            "minimum_age": 12,
            "shooting_permissions_needed": True,
        },
        {
            "class_id": "drama",
            "capacity_a": 15,
            "capacity_b": 15,
            "capacity_c": 15,
            "capacity_d": 15,
            "minimum_age": None,
            "shooting_permissions_needed": False,
        },
        {
            "class_id": "five_stand",
            "capacity_a": 0,
            "capacity_b": 1,
            "capacity_c": 15,
            "capacity_d": 15,
            "minimum_age": 14,
            "shooting_permissions_needed": True,
        },
        {
            "class_id": "paintball",
            "capacity_a": 10,
            "capacity_b": 10,
            "capacity_c": 10,
            "capacity_d": 0,
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
            class_id=class_raw['class_id'],
            capacity_a=class_raw['capacity_a'],
            capacity_b=class_raw['capacity_b'],
            capacity_c=class_raw['capacity_c'],
            capacity_d=class_raw['capacity_d'],
            minimum_age=class_raw['minimum_age'],
            shooting_permissions_needed=class_raw['shooting_permissions_needed']
        )
    
        assert class_.class_id == class_raw['class_id']
        assert class_.capacity_a == class_raw['capacity_a']
        assert class_.capacity_b == class_raw['capacity_b']
        assert class_.capacity_c == class_raw['capacity_c']
        assert class_.capacity_d == class_raw['capacity_d']
        assert class_.minimum_age == class_raw['minimum_age']
        assert class_.shooting_permissions_needed == class_raw['shooting_permissions_needed']
        assert len(class_.a) == 0
        assert len(class_.b) == 0
        assert len(class_.c) == 0
        assert len(class_.d) == 0
        
        
        
    def test_camper_object_populated(self, valid_classes):
        """Testing a class can be created with an object"""
        class_raw = valid_classes[1]
        class_ = Class(**class_raw)


        assert class_.class_id == class_raw['class_id']
        assert class_.capacity_a == class_raw['capacity_a']
        assert class_.capacity_b == class_raw['capacity_b']
        assert class_.capacity_c == class_raw['capacity_c']
        assert class_.capacity_d == class_raw['capacity_d']
        assert class_.minimum_age == class_raw['minimum_age']
        assert class_.shooting_permissions_needed == class_raw['shooting_permissions_needed']
        assert len(class_.a) == 0
        assert len(class_.b) == 0
        assert len(class_.c) == 0
        assert len(class_.d) == 0
        
class TestClassMethods:
    """Tests focused on how class properties/methods behave"""
    
    
    