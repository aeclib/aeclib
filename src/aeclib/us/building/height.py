from typing import Union

from aeclib.us.building.constants import (
    ALLOWABLE_HEIGHT_BY_OCCUPANCY,
    ALLOWABLE_STORIES_BY_OCCUPANCY,
)
from aeclib.us.building.utils import lookup_by_building_props
from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem


def _lookup_height_limit(
    occupancy: Occupancy, sprinkler_system: SprinklerSystem, construction_type: ConstructionType
) -> Union[float, str]:
    return lookup_by_building_props(
        ALLOWABLE_HEIGHT_BY_OCCUPANCY, occupancy, sprinkler_system, construction_type, "height"
    )


def _lookup_story_limit(
    occupancy: Occupancy, sprinkler_system: SprinklerSystem, construction_type: ConstructionType
) -> Union[int, str]:
    return lookup_by_building_props(
        ALLOWABLE_STORIES_BY_OCCUPANCY, occupancy, sprinkler_system, construction_type, "story"
    )


def get_allowable_height_feet(
    occupancy: Occupancy,
    construction_type: ConstructionType,
    sprinkler_system: SprinklerSystem,
    is_type_iiia_r_increase_applicable: bool = False,
) -> Union[float, str]:
    """
    Returns the allowable building height in feet above grade plane.

    Applicable to:
    - IBC 2024 Section 504.3
    - IBC 2024 Table 504.3

    Args:
        occupancy: The Occupancy classification.
        construction_type: The Construction Type.
        sprinkler_system: The type of sprinkler system installed.
        is_type_iiia_r_increase_applicable: True if the 10-foot increase for Type IIIA
            Group R buildings applies (Section 504.3 exception).

    Returns:
        The allowable height in feet as a float, or "UL" for unlimited.
    """
    base_height = _lookup_height_limit(occupancy, sprinkler_system, construction_type)

    # 504.3 Exception: 10 ft increase for Type IIIA Group R-1/R-2 under specific structural conditions
    if is_type_iiia_r_increase_applicable and isinstance(base_height, float):
        if construction_type == ConstructionType.TYPE_III_A and occupancy in [Occupancy.GROUP_R_1, Occupancy.GROUP_R_2]:
            return base_height + 10.0

    return base_height


def get_allowable_stories(
    occupancy: Occupancy,
    construction_type: ConstructionType,
    sprinkler_system: SprinklerSystem,
    is_type_iiia_r_increase_applicable: bool = False,
) -> Union[int, str]:
    """
    Returns the allowable number of stories above grade plane.

    Applicable to:
    - IBC 2024 Section 504.4
    - IBC 2024 Table 504.4

    Args:
        occupancy: The Occupancy classification.
        construction_type: The Construction Type.
        sprinkler_system: The type of sprinkler system installed.
        is_type_iiia_r_increase_applicable: True if the 1-story increase for Type IIIA
            Group R buildings applies (Section 504.4 exception).

    Returns:
        The allowable number of stories as an int, or "UL" for unlimited.
    """
    base_stories = _lookup_story_limit(occupancy, sprinkler_system, construction_type)

    # 504.4 Exception: 1 story increase for Type IIIA Group R-1/R-2 under specific structural conditions
    if is_type_iiia_r_increase_applicable and isinstance(base_stories, int):
        if construction_type == ConstructionType.TYPE_III_A and occupancy in [Occupancy.GROUP_R_1, Occupancy.GROUP_R_2]:
            return base_stories + 1

    return base_stories
