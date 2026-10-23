import pytest

from class_sorter.models.campers import Camper
from class_sorter.models.classes import Class
from class_sorter.services.assignment import AssignmentEngine


@pytest.fixture
def setup_objects():
    """Generate sample campers and classes for assignment tests"""
    c1 = Class(
        class_id="kayaking",
        minimum_age=None,
        period_capacities={"A": 1, "B": 1},
        shooting_permissions_needed=False,
    )

    camper1 = Camper(
        first_name="Barry",
        last_name="Allen",
        cabin="12",
        age=12,
        allowed_to_shoot=True,
        preferences=["kayaking"],
    )
    camper2 = Camper(
        first_name="Wally",
        last_name="West",
        cabin="12",
        age=11,
        allowed_to_shoot=True,
        preferences=["kayaking"],
    )

    return [camper1, camper2], [c1]


def test_assignment_determinism(setup_objects):
    """Make sure the test sorts the same way twice given the same seed."""

    campers, classes = setup_objects

    seed = 22

    # Run 1
    engine1 = AssignmentEngine(campers=campers, classes=classes)
    score1 = engine1.assign_greedy(seed)
    results1 = [
        [camper.first_name, len(camper.enrolled_sections)] for camper in campers
    ]

    engine1.reset()

    # Run 2
    engine2 = AssignmentEngine(campers=campers, classes=classes)
    score2 = engine2.assign_greedy(seed)
    results2 = [
        [camper.first_name, len(camper.enrolled_sections)] for camper in campers
    ]

    # Scores and campers should look the same
    assert score1 == score2
    assert results1 == results2


def test_reset_functionality(setup_objects):
    """Test that reset() restores campers and classes to original state."""
    campers, classes = setup_objects
    engine = AssignmentEngine(campers, classes)
    
    engine.assign_greedy(seed=22)
    
    # Verify something actually happened
    assert any(len(c.enrolled_sections) > 0 for c in campers)
    
    # Reset
    engine.reset()
    
    # Verify all campers have 0 sections
    for camper in campers:
        assert len(camper.enrolled_sections) == 0
        
    # Verify all classes have 0 campers in sections
    for c in classes:
        for section in c.sections.values():
            assert len(section.enrolled_campers) == 0