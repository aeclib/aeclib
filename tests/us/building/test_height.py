import pytest

from aeclib.us.building.height import get_allowable_height_feet, get_allowable_stories
from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem


def test_allowable_height_group_b_non_sprinklered():
    # Group B, Type IIB, Non-Sprinklered -> 55 feet
    assert (
        get_allowable_height_feet(Occupancy.GROUP_B, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED)
        == 55.0
    )


def test_allowable_height_group_b_sprinklered():
    # Group B, Type IIB, Sprinklered (S) -> 75 feet
    assert (
        get_allowable_height_feet(Occupancy.GROUP_B, ConstructionType.TYPE_II_B, SprinklerSystem.FULLY_SPRINKLERED)
        == 75.0
    )

    # Group B, Type IA, Sprinklered -> "UL" (Unlimited)
    assert (
        get_allowable_height_feet(Occupancy.GROUP_B, ConstructionType.TYPE_I_A, SprinklerSystem.FULLY_SPRINKLERED)
        == "UL"
    )


def test_allowable_height_group_r_sprinkler_systems():
    # Group R-2, Type VA, Non-Sprinklered -> 50 feet
    assert (
        get_allowable_height_feet(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_A, SprinklerSystem.NOT_SPRINKLERED)
        == 50.0
    )

    # Group R-2, Type VA, S13R -> 60 feet (Base table exception for S13R overriding Type V limits)
    assert (
        get_allowable_height_feet(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_A, SprinklerSystem.SPRINKLERED_13R)
        == 60.0
    )

    # Group R-2, Type VA, S13D -> 50 feet (Type V override for S13D)
    assert (
        get_allowable_height_feet(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_A, SprinklerSystem.SPRINKLERED_13D)
        == 50.0
    )


def test_type_iiia_r_increase():
    # Group R-2, Type IIIA, Non-Sprinklered -> Base is 65 feet.
    assert (
        get_allowable_height_feet(Occupancy.GROUP_R_2, ConstructionType.TYPE_III_A, SprinklerSystem.NOT_SPRINKLERED)
        == 65.0
    )

    # Group R-2, Type IIIA, Non-Sprinklered with the special 3-hour first-floor exception -> 75 feet
    assert (
        get_allowable_height_feet(
            Occupancy.GROUP_R_2,
            ConstructionType.TYPE_III_A,
            SprinklerSystem.NOT_SPRINKLERED,
            is_type_iiia_r_increase_applicable=True,
        )
        == 75.0
    )


def test_unimplemented_occupancy_raises_error():
    # We haven't encoded Group A-1 yet in TABLE_504_3
    with pytest.raises(NotImplementedError):
        get_allowable_height_feet(Occupancy.GROUP_A_1, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED)


def test_allowable_stories_group_b():
    # Group B, Type IIB, NS -> 3 stories
    assert get_allowable_stories(Occupancy.GROUP_B, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED) == 3

    # Group B, Type IIB, S -> 4 stories
    assert get_allowable_stories(Occupancy.GROUP_B, ConstructionType.TYPE_II_B, SprinklerSystem.FULLY_SPRINKLERED) == 4


def test_allowable_stories_group_r2_sprinklers():
    # Group R-2, Type VA, NS -> 3 stories
    assert get_allowable_stories(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_A, SprinklerSystem.NOT_SPRINKLERED) == 3

    # Group R-2, Type VA, S13R -> 4 stories
    assert get_allowable_stories(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_A, SprinklerSystem.SPRINKLERED_13R) == 4

    # Group R-2, Type VB, S13R -> 3 stories
    assert get_allowable_stories(Occupancy.GROUP_R_2, ConstructionType.TYPE_V_B, SprinklerSystem.SPRINKLERED_13R) == 3


def test_stories_type_iiia_r_increase():
    # Group R-2, Type IIIA, NS -> 4 stories
    assert get_allowable_stories(Occupancy.GROUP_R_2, ConstructionType.TYPE_III_A, SprinklerSystem.NOT_SPRINKLERED) == 4

    # With exception -> 5 stories
    assert (
        get_allowable_stories(
            Occupancy.GROUP_R_2,
            ConstructionType.TYPE_III_A,
            SprinklerSystem.NOT_SPRINKLERED,
            is_type_iiia_r_increase_applicable=True,
        )
        == 5
    )


def test_allowable_height_group_m():
    # Group M, Type IIB, NS -> 55 feet (Uses the General NS grouping)
    assert (
        get_allowable_height_feet(Occupancy.GROUP_M, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED)
        == 55.0
    )
