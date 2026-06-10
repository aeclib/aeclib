from typing import Optional, Union

from aeclib.us.building.constants import ALLOWABLE_AREA_BY_OCCUPANCY
from aeclib.us.building.utils import lookup_by_building_props
from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem


def _lookup_area_limit(
    occupancy: Occupancy, table_column: str, construction_type: ConstructionType
) -> Union[float, str]:
    return lookup_by_building_props(ALLOWABLE_AREA_BY_OCCUPANCY, occupancy, table_column, construction_type, "area")


def calculate_frontage_increase(
    perimeter_total: float, perimeter_open: float, open_width: float, is_section_507: bool = False
) -> float:
    """
    Calculates the area factor increase due to frontage (I_f).

    Applicable to:
    - IBC 2024 Section 506.3
    - IBC 2024 Table 506.3.3
    - IBC 2024 Table 506.3.3.1

    IBC 2024 represents this as a table with permitted interpolation.
    The mathematical equivalent (which was explicitly written in prior IBC editions) is:
    I_f = [F/P - 0.25] * (W / 30)

    Args:
        perimeter_total: Total perimeter of the building in feet (P).
        perimeter_open: Perimeter of the building adjoining open space in feet (F).
        open_width: Width of the public way or open space in feet (W).
        is_section_507: True if the building qualifies under Section 507 (Unlimited Area Buildings).

    Returns:
        float: The frontage increase factor (I_f).
    """
    if perimeter_total <= 0:
        return 0.0

    f_p_ratio = perimeter_open / perimeter_total

    # Must have at least 25% of perimeter open to qualify for any increase
    if f_p_ratio < 0.25:
        return 0.0

    if is_section_507:
        # Table 506.3.3.1 requires minimum 30 feet open space, caps at 60 feet (W/30 = 2.0)
        if open_width < 30.0:
            return 0.0
        w_factor = min(open_width / 30.0, 2.0)
    else:
        # Table 506.3.3 requires minimum 20 feet open space, caps at 30 feet (W/30 = 1.0)
        if open_width < 20.0:
            return 0.0
        w_factor = min(open_width / 30.0, 1.0)

    i_f = (f_p_ratio - 0.25) * w_factor

    return max(0.0, i_f)


def get_tabular_allowable_area(
    occupancy: Occupancy, construction_type: ConstructionType, sprinkler_system: SprinklerSystem, stories: int
) -> Union[float, str]:
    """
    Returns the tabular allowable area (At) in square feet.

    Applicable to:
    - IBC 2024 Section 506.2
    - IBC 2024 Table 506.2

    Args:
        occupancy: The Occupancy classification.
        construction_type: The Construction Type.
        sprinkler_system: The type of sprinkler system installed.
        stories: The total number of stories above grade plane.
                 (This determines if the S1 or SM multiplier applies).

    Returns:
        The tabular allowable area in square feet as a float, or "UL" for unlimited.
    """
    # Map sprinkler system and stories to the correct Table 506.2 column (NS, S1, or SM)
    table_column = "NS"
    if sprinkler_system == SprinklerSystem.FULLY_SPRINKLERED:
        table_column = "S1" if stories == 1 else "SM"
    elif sprinkler_system in [SprinklerSystem.SPRINKLERED_13R, SprinklerSystem.SPRINKLERED_13D]:
        # IBC 506.2.1: 13R and 13D systems use the NS value for allowable area
        table_column = "NS"

    return _lookup_area_limit(occupancy, table_column, construction_type)


def validate_story_area(
    actual_area: float,
    occupancy: Occupancy,
    construction_type: ConstructionType,
    sprinkler_system: SprinklerSystem,
    stories: int,
    frontage_increase: Optional[float] = None,
    perimeter_total: Optional[float] = None,
    perimeter_open: Optional[float] = None,
    open_width: Optional[float] = None,
    is_section_507: bool = False,
) -> bool:
    """
    Validates that a story's actual area is within the allowable limits of the IBC.

    Applicable to:
    - IBC 2024 Section 506.2
    - IBC 2024 Section 506.3

    Args:
        actual_area: The actual area of the story in square feet.
        occupancy: The Occupancy classification.
        construction_type: The Construction Type.
        sprinkler_system: The type of sprinkler system installed.
        stories: The total number of stories in the building.
        frontage_increase: Optional pre-calculated frontage increase factor (If).
        perimeter_total: Optional total building perimeter for frontage calculation.
        perimeter_open: Optional open building perimeter for frontage calculation.
        open_width: Optional open space width for frontage calculation.
        is_section_507: True if the building qualifies under Section 507.

    Returns:
        True if the actual area is <= total allowable area, False otherwise.
    """
    # 1. Resolve frontage increase
    if_factor = frontage_increase
    if if_factor is None:
        if all(v is not None for v in [perimeter_total, perimeter_open, open_width]):
            if_factor = calculate_frontage_increase(perimeter_total, perimeter_open, open_width, is_section_507)
        else:
            if_factor = 0.0

    # 2. Get tabular area (At)
    tabular_area = get_tabular_allowable_area(occupancy, construction_type, sprinkler_system, stories)

    if tabular_area == "UL":
        return True

    if not isinstance(tabular_area, float):
        raise ValueError(f"Unexpected tabular area type: {type(tabular_area)}")

    # 3. Calculate final limit (Aa)
    # Formula: Aa = At + (At * If)
    allowable_area = tabular_area + (tabular_area * if_factor)

    return actual_area <= allowable_area
