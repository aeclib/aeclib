from enum import Enum


class BuildingElementCategory(str, Enum):
    """
    IBC 2024 Building Element Categories.
    Currently used for determining fire-resistance requirements (Table 601) and material exceptions (Section 603).
    TODO: Need to evaluate if this enum will be compatible with other use cases.
    """

    # Structural Elements (Table 601)
    PRIMARY_STRUCTURAL_FRAME = "primary_structural_frame"
    BEARING_WALL_EXTERIOR = "bearing_wall_exterior"
    BEARING_WALL_INTERIOR = "bearing_wall_interior"
    NONBEARING_WALL_EXTERIOR = "nonbearing_wall_exterior"
    NONBEARING_WALL_INTERIOR = "nonbearing_wall_interior"
    FLOOR_CONSTRUCTION = "floor_construction"
    ROOF_CONSTRUCTION = "roof_construction"

    # Material exceptions (Section 603)
    THERMAL_INSULATION = "thermal_insulation"
    ROOF_COVERING = "roof_covering"
    INTERIOR_FINISH = "interior_finish"
    MILLWORK = "millwork"
