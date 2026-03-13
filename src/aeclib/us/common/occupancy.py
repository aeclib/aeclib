from enum import Enum


class OccupancyClassification(str, Enum):
    """
    Standardized occupancy classifications for building design.
    """

    GROUP_A = "A"  # Assembly
    GROUP_B = "B"  # Business
    GROUP_E = "E"  # Educational
    GROUP_F = "F"  # Factory
    GROUP_H = "H"  # High Hazard
    GROUP_I = "I"  # Institutional
    GROUP_M = "M"  # Mercantile
    # Residential (Note: Standard detached single-family homes are typically IRC)
    GROUP_R = "R"
    GROUP_S = "S"  # Storage
    GROUP_U = "U"  # Utility
