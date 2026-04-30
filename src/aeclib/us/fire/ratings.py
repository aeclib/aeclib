from typing import Union

from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.elements import BuildingElementCategory

# Maps (Element, ConstructionType) -> Rating
# Using floats for hours (e.g. 1.5). 'HT' for Heavy Timber.
REQUIRED_FIRE_RATINGS_BY_ELEMENT = {
    BuildingElementCategory.PRIMARY_STRUCTURAL_FRAME: {
        ConstructionType.TYPE_I_A: 3.0,
        ConstructionType.TYPE_I_B: 2.0,
        ConstructionType.TYPE_II_A: 1.0,
        ConstructionType.TYPE_II_B: 0.0,
        ConstructionType.TYPE_III_A: 1.0,
        ConstructionType.TYPE_III_B: 0.0,
        ConstructionType.TYPE_IV_A: 3.0,
        ConstructionType.TYPE_IV_B: 2.0,
        ConstructionType.TYPE_IV_C: 2.0,
        ConstructionType.TYPE_IV_HT: "HT",
        ConstructionType.TYPE_V_A: 1.0,
        ConstructionType.TYPE_V_B: 0.0,
    },
    BuildingElementCategory.BEARING_WALL_EXTERIOR: {
        ConstructionType.TYPE_I_A: 3.0,
        ConstructionType.TYPE_I_B: 2.0,
        ConstructionType.TYPE_II_A: 1.0,
        ConstructionType.TYPE_II_B: 0.0,
        ConstructionType.TYPE_III_A: 2.0,
        ConstructionType.TYPE_III_B: 2.0,
        ConstructionType.TYPE_IV_A: 3.0,
        ConstructionType.TYPE_IV_B: 2.0,
        ConstructionType.TYPE_IV_C: 2.0,
        ConstructionType.TYPE_IV_HT: 2.0,
        ConstructionType.TYPE_V_A: 1.0,
        ConstructionType.TYPE_V_B: 0.0,
    },
    BuildingElementCategory.BEARING_WALL_INTERIOR: {
        ConstructionType.TYPE_I_A: 3.0,
        ConstructionType.TYPE_I_B: 2.0,
        ConstructionType.TYPE_II_A: 1.0,
        ConstructionType.TYPE_II_B: 0.0,
        ConstructionType.TYPE_III_A: 1.0,
        ConstructionType.TYPE_III_B: 0.0,
        ConstructionType.TYPE_IV_A: 3.0,
        ConstructionType.TYPE_IV_B: 2.0,
        ConstructionType.TYPE_IV_C: 2.0,
        ConstructionType.TYPE_IV_HT: "1/HT",
        ConstructionType.TYPE_V_A: 1.0,
        ConstructionType.TYPE_V_B: 0.0,
    },
    BuildingElementCategory.NONBEARING_WALL_INTERIOR: {ct: 0.0 for ct in ConstructionType},
    BuildingElementCategory.FLOOR_CONSTRUCTION: {
        ConstructionType.TYPE_I_A: 2.0,
        ConstructionType.TYPE_I_B: 2.0,
        ConstructionType.TYPE_II_A: 1.0,
        ConstructionType.TYPE_II_B: 0.0,
        ConstructionType.TYPE_III_A: 1.0,
        ConstructionType.TYPE_III_B: 0.0,
        ConstructionType.TYPE_IV_A: 2.0,
        ConstructionType.TYPE_IV_B: 2.0,
        ConstructionType.TYPE_IV_C: 2.0,
        ConstructionType.TYPE_IV_HT: "HT",
        ConstructionType.TYPE_V_A: 1.0,
        ConstructionType.TYPE_V_B: 0.0,
    },
    BuildingElementCategory.ROOF_CONSTRUCTION: {
        ConstructionType.TYPE_I_A: 1.5,
        ConstructionType.TYPE_I_B: 1.0,
        ConstructionType.TYPE_II_A: 1.0,
        ConstructionType.TYPE_II_B: 0.0,
        ConstructionType.TYPE_III_A: 1.0,
        ConstructionType.TYPE_III_B: 0.0,
        ConstructionType.TYPE_IV_A: 1.5,
        ConstructionType.TYPE_IV_B: 1.0,
        ConstructionType.TYPE_IV_C: 1.0,
        ConstructionType.TYPE_IV_HT: "HT",
        ConstructionType.TYPE_V_A: 1.0,
        ConstructionType.TYPE_V_B: 0.0,
    },
}


def get_required_fire_resistance_rating(
    construction_type: ConstructionType,
    element_category: BuildingElementCategory,
    is_supporting_roof_only: bool = False,
) -> Union[float, str]:
    """
    Returns the required fire-resistance rating in hours.

    Applicable to:
    - IBC 2024 Section 602.1
    - IBC 2024 Table 601

    Values are typically floats (e.g. 1.0, 1.5).
    For Heavy Timber, returns strings like 'HT' or '1/HT'.

    Args:
        construction_type: The building construction type.
        element_category: The structural element category.
        is_supporting_roof_only: True if the element only supports a roof.

    Returns:
        Union[float, str].
    """

    # Exterior nonbearing walls are dictated by Table 705.5 based on fire separation distance.
    if element_category == BuildingElementCategory.NONBEARING_WALL_EXTERIOR:
        raise ValueError(
            "Exterior nonbearing wall ratings are based on fire separation distance per Table 705.5, not Table 601."
        )

    # Some categories (like Insulation) don't have ratings in Table 601
    if element_category not in REQUIRED_FIRE_RATINGS_BY_ELEMENT:
        raise ValueError(f"Category {element_category} does not have a Table 601 rating.")

    base_rating = REQUIRED_FIRE_RATINGS_BY_ELEMENT[element_category][construction_type]

    # Footnote a: Roof supports can be reduced by 1 hour where supporting a roof only.
    if is_supporting_roof_only and isinstance(base_rating, float):
        if element_category in [
            BuildingElementCategory.PRIMARY_STRUCTURAL_FRAME,
            BuildingElementCategory.BEARING_WALL_EXTERIOR,
            BuildingElementCategory.BEARING_WALL_INTERIOR,
        ]:
            return max(0.0, base_rating - 1.0)

    return base_rating
