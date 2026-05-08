from dataclasses import dataclass
from typing import List

from aeclib.us.building.area import get_tabular_allowable_area
from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem


@dataclass
class StoryOccupancyArea:
    occupancy: Occupancy
    actual_area: float


def validate_accessory_occupancy(accessory_area: float, total_story_area: float) -> bool:
    """
    Validates that an accessory occupancy does not exceed 10% of the area of the story
    in which it is located.

    Applicable to:
    - IBC 2024 Section 508.2.3

    Args:
        accessory_area: The actual area of the accessory occupancy.
        total_story_area: The total area of the story containing the accessory occupancy.

    Returns:
        True if the accessory area is within the 10% limit, False otherwise.
    """
    if total_story_area <= 0:
        return False
    return accessory_area <= (total_story_area * 0.10)


def calculate_allowable_area(tabular_area: float, frontage_increase: float) -> float:
    """
    Calculates the total allowable area per story.

    Applicable to:
    - IBC 2024 Section 506.2 (Equation 5-1)

    Formula: Aa = At + (At * If)

    Args:
        tabular_area: The base tabular area (At) from Table 506.2.
        frontage_increase: The frontage increase factor (If) from Section 506.3.

    Returns:
        The total allowable area (Aa).
    """
    return tabular_area + (tabular_area * frontage_increase)


def calculate_sum_of_ratios(
    occupancy_areas: List[StoryOccupancyArea],
    construction_type: ConstructionType,
    sprinkler_system: SprinklerSystem,
    stories: int,
    frontage_increase: float = 0.0,
) -> float:
    """
    Calculates the sum of ratios for separated mixed-use occupancies on a single story.

    Applicable to:
    - IBC 2024 Section 508.4.2

    Formula: Sum(Actual Area / Allowable Area)

    Args:
        occupancy_areas: A list of actual areas by occupancy on the story.
        construction_type: The Construction Type.
        sprinkler_system: The type of sprinkler system installed.
        stories: The total number of stories in the building.
        frontage_increase: The area factor increase due to frontage (If). Defaults to 0.0.

    Returns:
        The sum of ratios as a float. To comply with the code, this value must be <= 1.0.
    """
    sum_ratios = 0.0

    for occ_area in occupancy_areas:
        tabular_area = get_tabular_allowable_area(occ_area.occupancy, construction_type, sprinkler_system, stories)

        if tabular_area == "UL":
            # If the allowable area is Unlimited, the ratio for this occupancy is effectively 0.
            continue

        if not isinstance(tabular_area, float):
            raise ValueError(f"Unexpected tabular area type for {occ_area.occupancy}")

        allowable_area = calculate_allowable_area(tabular_area, frontage_increase)

        if allowable_area <= 0:
            raise ValueError(f"Calculated allowable area for {occ_area.occupancy} is zero or negative.")

        sum_ratios += occ_area.actual_area / allowable_area

    return sum_ratios


def validate_nonseparated_occupancies(
    occupancy_areas: List[StoryOccupancyArea],
    construction_type: ConstructionType,
    sprinkler_system: SprinklerSystem,
    stories: int,
    frontage_increase: float = 0.0,
) -> bool:
    """
    Validates a story with nonseparated occupancies.

    Applicable to:
    - IBC 2024 Section 508.3

    The allowable area for the story is based on the most restrictive
    allowable area of the occupancies present.

    Args:
        occupancy_areas: A list of actual areas by occupancy on the story.
        construction_type: The Construction Type.
        sprinkler_system: The type of sprinkler system installed.
        stories: The total number of stories in the building.
        frontage_increase: The area factor increase due to frontage (If). Defaults to 0.0.

    Returns:
        True if the total story area complies with the most restrictive limit.
    """
    if not occupancy_areas:
        return True

    total_actual_area = sum(occ.actual_area for occ in occupancy_areas)
    most_restrictive_allowable_area = float("inf")

    for occ in occupancy_areas:
        tabular_area = get_tabular_allowable_area(occ.occupancy, construction_type, sprinkler_system, stories)

        if tabular_area == "UL":
            continue

        if not isinstance(tabular_area, float):
            raise ValueError(f"Unexpected tabular area type for {occ.occupancy}")

        allowable_area = calculate_allowable_area(tabular_area, frontage_increase)

        if allowable_area < most_restrictive_allowable_area:
            most_restrictive_allowable_area = allowable_area

    if most_restrictive_allowable_area == float("inf"):
        return True

    return total_actual_area <= most_restrictive_allowable_area


def validate_separated_occupancies(
    occupancy_areas: List[StoryOccupancyArea],
    construction_type: ConstructionType,
    sprinkler_system: SprinklerSystem,
    stories: int,
    frontage_increase: float = 0.0,
) -> bool:
    """
    Validates a story with separated occupancies.

    Applicable to:
    - IBC 2024 Section 508.4

    The sum of ratios of actual area to allowable area must not exceed 1.0.

    Args:
        occupancy_areas: A list of actual areas by occupancy on the story.
        construction_type: The Construction Type.
        sprinkler_system: The type of sprinkler system installed.
        stories: The total number of stories in the building.
        frontage_increase: The area factor increase due to frontage (If). Defaults to 0.0.

    Returns:
        True if the sum of ratios is <= 1.0.
    """
    sum_ratios = calculate_sum_of_ratios(
        occupancy_areas, construction_type, sprinkler_system, stories, frontage_increase
    )
    return sum_ratios <= 1.0
