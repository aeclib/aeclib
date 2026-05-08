from aeclib.us.building.area import calculate_frontage_increase, get_tabular_allowable_area, validate_story_area
from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem


def test_frontage_increase_standard():
    # 100% perimeter open, W = 30 feet
    # [1.0 - 0.25] * (30/30) = 0.75
    assert calculate_frontage_increase(400, 400, 30) == 0.75

    # 50% perimeter open, W = 30 feet
    # [0.5 - 0.25] * (30/30) = 0.25
    assert calculate_frontage_increase(400, 200, 30) == 0.25

    # 100% perimeter open, W = 20 feet
    # [1.0 - 0.25] * (20/30) = 0.50
    assert calculate_frontage_increase(400, 400, 20) == 0.50


def test_frontage_increase_caps():
    # W is capped at 30 for standard buildings
    # [1.0 - 0.25] * min(50/30, 1.0) = 0.75
    assert calculate_frontage_increase(400, 400, 50) == 0.75


def test_frontage_increase_minimums():
    # Less than 25% perimeter open -> 0 increase
    assert calculate_frontage_increase(400, 50, 30) == 0.0

    # Less than 20 feet open width -> 0 increase
    assert calculate_frontage_increase(400, 400, 15) == 0.0


def test_frontage_increase_section_507():
    # 100% perimeter open, W = 60 feet
    # [1.0 - 0.25] * (60/30) = 1.50
    assert calculate_frontage_increase(400, 400, 60, is_section_507=True) == 1.50

    # Section 507 W capped at 60 (factor of 2.0)
    assert calculate_frontage_increase(400, 400, 100, is_section_507=True) == 1.50

    # Section 507 minimum W is 30. If less than 30, it is 0.
    assert calculate_frontage_increase(400, 400, 25, is_section_507=True) == 0.0


def test_tabular_area_group_b():
    # Group B, Type IIB, NS, 1 story -> 23000
    assert (
        get_tabular_allowable_area(Occupancy.GROUP_B, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED, 1)
        == 23000.0
    )

    # Group B, Type IIB, S, 1 story -> 92000 (S1)
    assert (
        get_tabular_allowable_area(Occupancy.GROUP_B, ConstructionType.TYPE_II_B, SprinklerSystem.FULLY_SPRINKLERED, 1)
        == 92000.0
    )

    # Group B, Type IIB, S, 2 stories -> 69000 (SM)
    assert (
        get_tabular_allowable_area(Occupancy.GROUP_B, ConstructionType.TYPE_II_B, SprinklerSystem.FULLY_SPRINKLERED, 2)
        == 69000.0
    )


def test_tabular_area_group_r2_13r():
    # Group R2, Type VA, 13R, 3 stories -> Falls back to NS -> 12000.0
    assert (
        get_tabular_allowable_area(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_A, SprinklerSystem.SPRINKLERED_13R, 3)
        == 12000.0
    )

    # Group R2, Type VA, 13D, 2 stories -> Falls back to NS -> 12000.0
    assert (
        get_tabular_allowable_area(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_A, SprinklerSystem.SPRINKLERED_13D, 2)
        == 12000.0
    )


def test_validate_story_area():
    # Group B, Type IIB, NS -> Tabular Area = 23,000
    # Actual area = 30,000
    # Perimeter = 600, Open = 450, Width = 25 -> If = 0.5625
    # Allowable = 23,000 * 1.5625 = 35,937.5

    # 1. Test failure without frontage
    assert not validate_story_area(
        actual_area=30000,
        occupancy=Occupancy.GROUP_B,
        construction_type=ConstructionType.TYPE_II_B,
        sprinkler_system=SprinklerSystem.NOT_SPRINKLERED,
        stories=1,
    )

    # 2. Test success with site data
    assert validate_story_area(
        actual_area=30000,
        occupancy=Occupancy.GROUP_B,
        construction_type=ConstructionType.TYPE_II_B,
        sprinkler_system=SprinklerSystem.NOT_SPRINKLERED,
        stories=1,
        perimeter_total=600,
        perimeter_open=450,
        open_width=25,
    )

    # 3. Test success with pre-calculated factor
    assert validate_story_area(
        actual_area=30000,
        occupancy=Occupancy.GROUP_B,
        construction_type=ConstructionType.TYPE_II_B,
        sprinkler_system=SprinklerSystem.NOT_SPRINKLERED,
        stories=1,
        frontage_increase=0.5625,
    )
