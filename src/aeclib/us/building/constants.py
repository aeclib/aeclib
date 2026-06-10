from typing import Dict, Union

from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem

# Helper type for tabular height data
# Mapping: ConstructionType -> height in feet (float) or 'UL' for Unlimited
HeightData = Dict[ConstructionType, Union[float, str]]

# Table 504.3: Allowable Building Height in Feet Above Grade Plane
# We use a nested dictionary: Occupancy -> SprinklerSystem -> HeightData
# To avoid massive repetition, we define base arrays for common occupancy groupings.

# General grouping covering A, B, E, F, M, S, U
_HEIGHT_GENERAL_NS: HeightData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 160.0,
    ConstructionType.TYPE_II_A: 65.0,
    ConstructionType.TYPE_II_B: 55.0,
    ConstructionType.TYPE_III_A: 65.0,
    ConstructionType.TYPE_III_B: 55.0,
    ConstructionType.TYPE_IV_A: 65.0,
    ConstructionType.TYPE_IV_B: 65.0,
    ConstructionType.TYPE_IV_C: 65.0,
    ConstructionType.TYPE_IV_HT: 65.0,
    ConstructionType.TYPE_V_A: 50.0,
    ConstructionType.TYPE_V_B: 40.0,
}

_HEIGHT_GENERAL_S: HeightData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 180.0,
    ConstructionType.TYPE_II_A: 85.0,
    ConstructionType.TYPE_II_B: 75.0,
    ConstructionType.TYPE_III_A: 85.0,
    ConstructionType.TYPE_III_B: 75.0,
    ConstructionType.TYPE_IV_A: 270.0,
    ConstructionType.TYPE_IV_B: 180.0,
    ConstructionType.TYPE_IV_C: 85.0,
    ConstructionType.TYPE_IV_HT: 85.0,
    ConstructionType.TYPE_V_A: 70.0,
    ConstructionType.TYPE_V_B: 60.0,
}

# Residential grouping covering R-1, R-2, R-3, R-4
_HEIGHT_RESIDENTIAL_NS: HeightData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 160.0,
    ConstructionType.TYPE_II_A: 65.0,
    ConstructionType.TYPE_II_B: 55.0,
    ConstructionType.TYPE_III_A: 65.0,
    ConstructionType.TYPE_III_B: 55.0,
    ConstructionType.TYPE_IV_A: 65.0,
    ConstructionType.TYPE_IV_B: 65.0,
    ConstructionType.TYPE_IV_C: 65.0,
    ConstructionType.TYPE_IV_HT: 65.0,
    ConstructionType.TYPE_V_A: 50.0,
    ConstructionType.TYPE_V_B: 40.0,
}

_HEIGHT_RESIDENTIAL_S13D: HeightData = {ct: 60.0 for ct in ConstructionType}
# Override Type V for 13D
_HEIGHT_RESIDENTIAL_S13D[ConstructionType.TYPE_V_A] = 50.0
_HEIGHT_RESIDENTIAL_S13D[ConstructionType.TYPE_V_B] = 40.0

_HEIGHT_RESIDENTIAL_S13R: HeightData = {ct: 60.0 for ct in ConstructionType}

_HEIGHT_RESIDENTIAL_S: HeightData = _HEIGHT_GENERAL_S

ALLOWABLE_HEIGHT_BY_OCCUPANCY = {
    # General grouping: A, B, E, F, M, S, U share the same tabular height limits
    Occupancy.GROUP_A: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_GENERAL_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_GENERAL_S,
    },
    Occupancy.GROUP_B: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_GENERAL_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_GENERAL_S,
    },
    Occupancy.GROUP_E: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_GENERAL_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_GENERAL_S,
    },
    Occupancy.GROUP_F: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_GENERAL_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_GENERAL_S,
    },
    Occupancy.GROUP_M: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_GENERAL_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_GENERAL_S,
    },
    Occupancy.GROUP_S: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_GENERAL_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_GENERAL_S,
    },
    Occupancy.GROUP_U: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_GENERAL_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_GENERAL_S,
    },
    # Residential grouping covering R-1, R-2, R-3, R-4
    Occupancy.GROUP_R_1: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_RESIDENTIAL_NS,
        SprinklerSystem.SPRINKLERED_13D: _HEIGHT_RESIDENTIAL_S13D,
        SprinklerSystem.SPRINKLERED_13R: _HEIGHT_RESIDENTIAL_S13R,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_RESIDENTIAL_S,
    },
    Occupancy.GROUP_R_2: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_RESIDENTIAL_NS,
        SprinklerSystem.SPRINKLERED_13D: _HEIGHT_RESIDENTIAL_S13D,
        SprinklerSystem.SPRINKLERED_13R: _HEIGHT_RESIDENTIAL_S13R,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_RESIDENTIAL_S,
    },
    Occupancy.GROUP_R_3: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_RESIDENTIAL_NS,
        SprinklerSystem.SPRINKLERED_13D: _HEIGHT_RESIDENTIAL_S13D,
        SprinklerSystem.SPRINKLERED_13R: _HEIGHT_RESIDENTIAL_S13R,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_RESIDENTIAL_S,
    },
    Occupancy.GROUP_R_4: {
        SprinklerSystem.NOT_SPRINKLERED: _HEIGHT_RESIDENTIAL_NS,
        SprinklerSystem.SPRINKLERED_13D: _HEIGHT_RESIDENTIAL_S13D,
        SprinklerSystem.SPRINKLERED_13R: _HEIGHT_RESIDENTIAL_S13R,
        SprinklerSystem.FULLY_SPRINKLERED: _HEIGHT_RESIDENTIAL_S,
    },
}

# Helper type for tabular story data
# Mapping: ConstructionType -> stories (int) or 'UL' for Unlimited
StoryData = Dict[ConstructionType, Union[int, str]]

_STORIES_BUSINESS_NS: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 11,
    ConstructionType.TYPE_II_A: 5,
    ConstructionType.TYPE_II_B: 3,
    ConstructionType.TYPE_III_A: 5,
    ConstructionType.TYPE_III_B: 3,
    ConstructionType.TYPE_IV_A: 5,
    ConstructionType.TYPE_IV_B: 5,
    ConstructionType.TYPE_IV_C: 5,
    ConstructionType.TYPE_IV_HT: 5,
    ConstructionType.TYPE_V_A: 3,
    ConstructionType.TYPE_V_B: 2,
}

_STORIES_BUSINESS_S: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 12,
    ConstructionType.TYPE_II_A: 6,
    ConstructionType.TYPE_II_B: 4,
    ConstructionType.TYPE_III_A: 6,
    ConstructionType.TYPE_III_B: 4,
    ConstructionType.TYPE_IV_A: 18,
    ConstructionType.TYPE_IV_B: 12,
    ConstructionType.TYPE_IV_C: 9,
    ConstructionType.TYPE_IV_HT: 6,
    ConstructionType.TYPE_V_A: 4,
    ConstructionType.TYPE_V_B: 3,
}

_STORIES_RESIDENTIAL_R2_NS: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 11,
    ConstructionType.TYPE_II_A: 4,
    ConstructionType.TYPE_II_B: 4,
    ConstructionType.TYPE_III_A: 4,
    ConstructionType.TYPE_III_B: 4,
    ConstructionType.TYPE_IV_A: 4,
    ConstructionType.TYPE_IV_B: 4,
    ConstructionType.TYPE_IV_C: 4,
    ConstructionType.TYPE_IV_HT: 4,
    ConstructionType.TYPE_V_A: 3,
    ConstructionType.TYPE_V_B: 2,
}

_STORIES_RESIDENTIAL_R2_S13R: StoryData = {ct: 4 for ct in ConstructionType}
_STORIES_RESIDENTIAL_R2_S13R[ConstructionType.TYPE_V_B] = 3

_STORIES_RESIDENTIAL_R2_S: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 12,
    ConstructionType.TYPE_II_A: 5,
    ConstructionType.TYPE_II_B: 5,
    ConstructionType.TYPE_III_A: 5,
    ConstructionType.TYPE_III_B: 5,
    ConstructionType.TYPE_IV_A: 18,
    ConstructionType.TYPE_IV_B: 12,
    ConstructionType.TYPE_IV_C: 8,
    ConstructionType.TYPE_IV_HT: 5,
    ConstructionType.TYPE_V_A: 4,
    ConstructionType.TYPE_V_B: 3,
}

_STORIES_MERCANTILE_NS: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 11,
    ConstructionType.TYPE_II_A: 4,
    ConstructionType.TYPE_II_B: 2,
    ConstructionType.TYPE_III_A: 4,
    ConstructionType.TYPE_III_B: 2,
    ConstructionType.TYPE_IV_A: 4,
    ConstructionType.TYPE_IV_B: 4,
    ConstructionType.TYPE_IV_C: 4,
    ConstructionType.TYPE_IV_HT: 4,
    ConstructionType.TYPE_V_A: 3,
    ConstructionType.TYPE_V_B: 1,
}

_STORIES_MERCANTILE_S: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 12,
    ConstructionType.TYPE_II_A: 5,
    ConstructionType.TYPE_II_B: 3,
    ConstructionType.TYPE_III_A: 5,
    ConstructionType.TYPE_III_B: 3,
    ConstructionType.TYPE_IV_A: 12,
    ConstructionType.TYPE_IV_B: 8,
    ConstructionType.TYPE_IV_C: 6,
    ConstructionType.TYPE_IV_HT: 5,
    ConstructionType.TYPE_V_A: 4,
    ConstructionType.TYPE_V_B: 2,
}

_STORIES_EDUCATION_NS: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 5,
    ConstructionType.TYPE_II_A: 3,
    ConstructionType.TYPE_II_B: 2,
    ConstructionType.TYPE_III_A: 3,
    ConstructionType.TYPE_III_B: 2,
    ConstructionType.TYPE_IV_A: 3,
    ConstructionType.TYPE_IV_B: 3,
    ConstructionType.TYPE_IV_C: 3,
    ConstructionType.TYPE_IV_HT: 3,
    ConstructionType.TYPE_V_A: 1,
    ConstructionType.TYPE_V_B: 1,
}

_STORIES_EDUCATION_S: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 6,
    ConstructionType.TYPE_II_A: 4,
    ConstructionType.TYPE_II_B: 3,
    ConstructionType.TYPE_III_A: 4,
    ConstructionType.TYPE_III_B: 3,
    ConstructionType.TYPE_IV_A: 9,
    ConstructionType.TYPE_IV_B: 6,
    ConstructionType.TYPE_IV_C: 4,
    ConstructionType.TYPE_IV_HT: 4,
    ConstructionType.TYPE_V_A: 2,
    ConstructionType.TYPE_V_B: 2,
}

_STORIES_STORAGE_S1_NS: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 11,
    ConstructionType.TYPE_II_A: 4,
    ConstructionType.TYPE_II_B: 2,
    ConstructionType.TYPE_III_A: 3,
    ConstructionType.TYPE_III_B: 2,
    ConstructionType.TYPE_IV_A: 4,
    ConstructionType.TYPE_IV_B: 4,
    ConstructionType.TYPE_IV_C: 4,
    ConstructionType.TYPE_IV_HT: 4,
    ConstructionType.TYPE_V_A: 3,
    ConstructionType.TYPE_V_B: 1,
}

_STORIES_STORAGE_S1_S: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 12,
    ConstructionType.TYPE_II_A: 5,
    ConstructionType.TYPE_II_B: 4,
    ConstructionType.TYPE_III_A: 4,
    ConstructionType.TYPE_III_B: 4,
    ConstructionType.TYPE_IV_A: 10,
    ConstructionType.TYPE_IV_B: 7,
    ConstructionType.TYPE_IV_C: 5,
    ConstructionType.TYPE_IV_HT: 5,
    ConstructionType.TYPE_V_A: 4,
    ConstructionType.TYPE_V_B: 2,
}

_STORIES_STORAGE_S2_NS: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 11,
    ConstructionType.TYPE_II_A: 5,
    ConstructionType.TYPE_II_B: 3,
    ConstructionType.TYPE_III_A: 4,
    ConstructionType.TYPE_III_B: 3,
    ConstructionType.TYPE_IV_A: 4,
    ConstructionType.TYPE_IV_B: 4,
    ConstructionType.TYPE_IV_C: 4,
    ConstructionType.TYPE_IV_HT: 5,
    ConstructionType.TYPE_V_A: 4,
    ConstructionType.TYPE_V_B: 2,
}

_STORIES_STORAGE_S2_S: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 12,
    ConstructionType.TYPE_II_A: 6,
    ConstructionType.TYPE_II_B: 4,
    ConstructionType.TYPE_III_A: 5,
    ConstructionType.TYPE_III_B: 4,
    ConstructionType.TYPE_IV_A: 12,
    ConstructionType.TYPE_IV_B: 8,
    ConstructionType.TYPE_IV_C: 5,
    ConstructionType.TYPE_IV_HT: 6,
    ConstructionType.TYPE_V_A: 5,
    ConstructionType.TYPE_V_B: 3,
}

_STORIES_UTILITY_NS: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 5,
    ConstructionType.TYPE_II_A: 4,
    ConstructionType.TYPE_II_B: 2,
    ConstructionType.TYPE_III_A: 3,
    ConstructionType.TYPE_III_B: 2,
    ConstructionType.TYPE_IV_A: 4,
    ConstructionType.TYPE_IV_B: 4,
    ConstructionType.TYPE_IV_C: 4,
    ConstructionType.TYPE_IV_HT: 4,
    ConstructionType.TYPE_V_A: 2,
    ConstructionType.TYPE_V_B: 1,
}

_STORIES_UTILITY_S: StoryData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 6,
    ConstructionType.TYPE_II_A: 5,
    ConstructionType.TYPE_II_B: 3,
    ConstructionType.TYPE_III_A: 4,
    ConstructionType.TYPE_III_B: 3,
    ConstructionType.TYPE_IV_A: 9,
    ConstructionType.TYPE_IV_B: 6,
    ConstructionType.TYPE_IV_C: 5,
    ConstructionType.TYPE_IV_HT: 5,
    ConstructionType.TYPE_V_A: 3,
    ConstructionType.TYPE_V_B: 2,
}

ALLOWABLE_STORIES_BY_OCCUPANCY = {
    Occupancy.GROUP_B: {
        SprinklerSystem.NOT_SPRINKLERED: _STORIES_BUSINESS_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _STORIES_BUSINESS_S,
    },
    Occupancy.GROUP_E: {
        SprinklerSystem.NOT_SPRINKLERED: _STORIES_EDUCATION_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _STORIES_EDUCATION_S,
    },
    Occupancy.GROUP_M: {
        SprinklerSystem.NOT_SPRINKLERED: _STORIES_MERCANTILE_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _STORIES_MERCANTILE_S,
    },
    Occupancy.GROUP_R_2: {
        SprinklerSystem.NOT_SPRINKLERED: _STORIES_RESIDENTIAL_R2_NS,
        SprinklerSystem.SPRINKLERED_13R: _STORIES_RESIDENTIAL_R2_S13R,
        SprinklerSystem.FULLY_SPRINKLERED: _STORIES_RESIDENTIAL_R2_S,
    },
    Occupancy.GROUP_S_1: {
        SprinklerSystem.NOT_SPRINKLERED: _STORIES_STORAGE_S1_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _STORIES_STORAGE_S1_S,
    },
    Occupancy.GROUP_S_2: {
        SprinklerSystem.NOT_SPRINKLERED: _STORIES_STORAGE_S2_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _STORIES_STORAGE_S2_S,
    },
    Occupancy.GROUP_U: {
        SprinklerSystem.NOT_SPRINKLERED: _STORIES_UTILITY_NS,
        SprinklerSystem.FULLY_SPRINKLERED: _STORIES_UTILITY_S,
    },
}

# Helper type for tabular area data
# Mapping: ConstructionType -> area in sq ft (float) or 'UL' for Unlimited
AreaData = Dict[ConstructionType, Union[float, str]]

_AREA_BUSINESS_NS: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 37500.0,
    ConstructionType.TYPE_II_B: 23000.0,
    ConstructionType.TYPE_III_A: 28500.0,
    ConstructionType.TYPE_III_B: 19000.0,
    ConstructionType.TYPE_IV_A: 108000.0,
    ConstructionType.TYPE_IV_B: 72000.0,
    ConstructionType.TYPE_IV_C: 45000.0,
    ConstructionType.TYPE_IV_HT: 36000.0,
    ConstructionType.TYPE_V_A: 18000.0,
    ConstructionType.TYPE_V_B: 9000.0,
}

_AREA_BUSINESS_S1: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 150000.0,
    ConstructionType.TYPE_II_B: 92000.0,
    ConstructionType.TYPE_III_A: 114000.0,
    ConstructionType.TYPE_III_B: 76000.0,
    ConstructionType.TYPE_IV_A: 432000.0,
    ConstructionType.TYPE_IV_B: 288000.0,
    ConstructionType.TYPE_IV_C: 180000.0,
    ConstructionType.TYPE_IV_HT: 144000.0,
    ConstructionType.TYPE_V_A: 72000.0,
    ConstructionType.TYPE_V_B: 36000.0,
}

_AREA_BUSINESS_SM: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 112500.0,
    ConstructionType.TYPE_II_B: 69000.0,
    ConstructionType.TYPE_III_A: 85500.0,
    ConstructionType.TYPE_III_B: 57000.0,
    ConstructionType.TYPE_IV_A: 324000.0,
    ConstructionType.TYPE_IV_B: 216000.0,
    ConstructionType.TYPE_IV_C: 135000.0,
    ConstructionType.TYPE_IV_HT: 108000.0,
    ConstructionType.TYPE_V_A: 54000.0,
    ConstructionType.TYPE_V_B: 27000.0,
}

_AREA_RESIDENTIAL_R2_NS: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 24000.0,
    ConstructionType.TYPE_II_B: 16000.0,
    ConstructionType.TYPE_III_A: 24000.0,
    ConstructionType.TYPE_III_B: 16000.0,
    ConstructionType.TYPE_IV_A: 61500.0,
    ConstructionType.TYPE_IV_B: 41000.0,
    ConstructionType.TYPE_IV_C: 25625.0,
    ConstructionType.TYPE_IV_HT: 20500.0,
    ConstructionType.TYPE_V_A: 12000.0,
    ConstructionType.TYPE_V_B: 7000.0,
}

_AREA_RESIDENTIAL_R2_S1: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 96000.0,
    ConstructionType.TYPE_II_B: 64000.0,
    ConstructionType.TYPE_III_A: 96000.0,
    ConstructionType.TYPE_III_B: 64000.0,
    ConstructionType.TYPE_IV_A: 246000.0,
    ConstructionType.TYPE_IV_B: 164000.0,
    ConstructionType.TYPE_IV_C: 102500.0,
    ConstructionType.TYPE_IV_HT: 82000.0,
    ConstructionType.TYPE_V_A: 48000.0,
    ConstructionType.TYPE_V_B: 28000.0,
}

_AREA_RESIDENTIAL_R2_SM: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 72000.0,
    ConstructionType.TYPE_II_B: 48000.0,
    ConstructionType.TYPE_III_A: 72000.0,
    ConstructionType.TYPE_III_B: 48000.0,
    ConstructionType.TYPE_IV_A: 184500.0,
    ConstructionType.TYPE_IV_B: 123000.0,
    ConstructionType.TYPE_IV_C: 76875.0,
    ConstructionType.TYPE_IV_HT: 61500.0,
    ConstructionType.TYPE_V_A: 36000.0,
    ConstructionType.TYPE_V_B: 21000.0,
}

_AREA_MERCANTILE_NS: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 21500.0,
    ConstructionType.TYPE_II_B: 12500.0,
    ConstructionType.TYPE_III_A: 18500.0,
    ConstructionType.TYPE_III_B: 12500.0,
    ConstructionType.TYPE_IV_A: 61500.0,
    ConstructionType.TYPE_IV_B: 41000.0,
    ConstructionType.TYPE_IV_C: 25625.0,
    ConstructionType.TYPE_IV_HT: 20500.0,
    ConstructionType.TYPE_V_A: 14000.0,
    ConstructionType.TYPE_V_B: 9000.0,
}

_AREA_MERCANTILE_S1: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 86000.0,
    ConstructionType.TYPE_II_B: 50000.0,
    ConstructionType.TYPE_III_A: 74000.0,
    ConstructionType.TYPE_III_B: 50000.0,
    ConstructionType.TYPE_IV_A: 246000.0,
    ConstructionType.TYPE_IV_B: 164000.0,
    ConstructionType.TYPE_IV_C: 102500.0,
    ConstructionType.TYPE_IV_HT: 82000.0,
    ConstructionType.TYPE_V_A: 56000.0,
    ConstructionType.TYPE_V_B: 36000.0,
}

_AREA_MERCANTILE_SM: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 64500.0,
    ConstructionType.TYPE_II_B: 37500.0,
    ConstructionType.TYPE_III_A: 55500.0,
    ConstructionType.TYPE_III_B: 37500.0,
    ConstructionType.TYPE_IV_A: 184500.0,
    ConstructionType.TYPE_IV_B: 123000.0,
    ConstructionType.TYPE_IV_C: 76875.0,
    ConstructionType.TYPE_IV_HT: 61500.0,
    ConstructionType.TYPE_V_A: 42000.0,
    ConstructionType.TYPE_V_B: 27000.0,
}

_AREA_EDUCATION_NS: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 26500.0,
    ConstructionType.TYPE_II_B: 14500.0,
    ConstructionType.TYPE_III_A: 23500.0,
    ConstructionType.TYPE_III_B: 14500.0,
    ConstructionType.TYPE_IV_A: 76500.0,
    ConstructionType.TYPE_IV_B: 51000.0,
    ConstructionType.TYPE_IV_C: 31875.0,
    ConstructionType.TYPE_IV_HT: 25500.0,
    ConstructionType.TYPE_V_A: 18500.0,
    ConstructionType.TYPE_V_B: 9500.0,
}

_AREA_EDUCATION_S1: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 106000.0,
    ConstructionType.TYPE_II_B: 58000.0,
    ConstructionType.TYPE_III_A: 94000.0,
    ConstructionType.TYPE_III_B: 58000.0,
    ConstructionType.TYPE_IV_A: 306000.0,
    ConstructionType.TYPE_IV_B: 204000.0,
    ConstructionType.TYPE_IV_C: 127500.0,
    ConstructionType.TYPE_IV_HT: 102000.0,
    ConstructionType.TYPE_V_A: 74000.0,
    ConstructionType.TYPE_V_B: 38000.0,
}

_AREA_EDUCATION_SM: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 79500.0,
    ConstructionType.TYPE_II_B: 43500.0,
    ConstructionType.TYPE_III_A: 70500.0,
    ConstructionType.TYPE_III_B: 43500.0,
    ConstructionType.TYPE_IV_A: 229500.0,
    ConstructionType.TYPE_IV_B: 153000.0,
    ConstructionType.TYPE_IV_C: 95625.0,
    ConstructionType.TYPE_IV_HT: 76500.0,
    ConstructionType.TYPE_V_A: 55500.0,
    ConstructionType.TYPE_V_B: 28500.0,
}

_AREA_STORAGE_S1_NS: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 26000.0,
    ConstructionType.TYPE_II_B: 17500.0,
    ConstructionType.TYPE_III_A: 26000.0,
    ConstructionType.TYPE_III_B: 17500.0,
    ConstructionType.TYPE_IV_A: 76500.0,
    ConstructionType.TYPE_IV_B: 51000.0,
    ConstructionType.TYPE_IV_C: 31875.0,
    ConstructionType.TYPE_IV_HT: 25500.0,
    ConstructionType.TYPE_V_A: 14000.0,
    ConstructionType.TYPE_V_B: 9000.0,
}

_AREA_STORAGE_S1_S1: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 104000.0,
    ConstructionType.TYPE_II_B: 70000.0,
    ConstructionType.TYPE_III_A: 104000.0,
    ConstructionType.TYPE_III_B: 70000.0,
    ConstructionType.TYPE_IV_A: 306000.0,
    ConstructionType.TYPE_IV_B: 204000.0,
    ConstructionType.TYPE_IV_C: 127500.0,
    ConstructionType.TYPE_IV_HT: 102000.0,
    ConstructionType.TYPE_V_A: 56000.0,
    ConstructionType.TYPE_V_B: 36000.0,
}

_AREA_STORAGE_S1_SM: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 78000.0,
    ConstructionType.TYPE_II_B: 52500.0,
    ConstructionType.TYPE_III_A: 78000.0,
    ConstructionType.TYPE_III_B: 52500.0,
    ConstructionType.TYPE_IV_A: 229500.0,
    ConstructionType.TYPE_IV_B: 153000.0,
    ConstructionType.TYPE_IV_C: 95625.0,
    ConstructionType.TYPE_IV_HT: 76500.0,
    ConstructionType.TYPE_V_A: 42000.0,
    ConstructionType.TYPE_V_B: 27000.0,
}

_AREA_STORAGE_S2_NS: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 39000.0,
    ConstructionType.TYPE_II_B: 26000.0,
    ConstructionType.TYPE_III_A: 39000.0,
    ConstructionType.TYPE_III_B: 26000.0,
    ConstructionType.TYPE_IV_A: 115500.0,
    ConstructionType.TYPE_IV_B: 77000.0,
    ConstructionType.TYPE_IV_C: 48125.0,
    ConstructionType.TYPE_IV_HT: 38500.0,
    ConstructionType.TYPE_V_A: 21000.0,
    ConstructionType.TYPE_V_B: 13500.0,
}

_AREA_STORAGE_S2_S1: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 156000.0,
    ConstructionType.TYPE_II_B: 104000.0,
    ConstructionType.TYPE_III_A: 156000.0,
    ConstructionType.TYPE_III_B: 104000.0,
    ConstructionType.TYPE_IV_A: 462000.0,
    ConstructionType.TYPE_IV_B: 308000.0,
    ConstructionType.TYPE_IV_C: 192500.0,
    ConstructionType.TYPE_IV_HT: 154000.0,
    ConstructionType.TYPE_V_A: 84000.0,
    ConstructionType.TYPE_V_B: 54000.0,
}

_AREA_STORAGE_S2_SM: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: "UL",
    ConstructionType.TYPE_II_A: 117000.0,
    ConstructionType.TYPE_II_B: 78000.0,
    ConstructionType.TYPE_III_A: 117000.0,
    ConstructionType.TYPE_III_B: 78000.0,
    ConstructionType.TYPE_IV_A: 346500.0,
    ConstructionType.TYPE_IV_B: 231000.0,
    ConstructionType.TYPE_IV_C: 144375.0,
    ConstructionType.TYPE_IV_HT: 115500.0,
    ConstructionType.TYPE_V_A: 63000.0,
    ConstructionType.TYPE_V_B: 40500.0,
}

_AREA_UTILITY_NS: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 35500.0,
    ConstructionType.TYPE_II_A: 19000.0,
    ConstructionType.TYPE_II_B: 8500.0,
    ConstructionType.TYPE_III_A: 14000.0,
    ConstructionType.TYPE_III_B: 8500.0,
    ConstructionType.TYPE_IV_A: 54000.0,
    ConstructionType.TYPE_IV_B: 36000.0,
    ConstructionType.TYPE_IV_C: 22500.0,
    ConstructionType.TYPE_IV_HT: 18000.0,
    ConstructionType.TYPE_V_A: 9000.0,
    ConstructionType.TYPE_V_B: 5500.0,
}

_AREA_UTILITY_S1: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 142000.0,
    ConstructionType.TYPE_II_A: 76000.0,
    ConstructionType.TYPE_II_B: 34000.0,
    ConstructionType.TYPE_III_A: 56000.0,
    ConstructionType.TYPE_III_B: 34000.0,
    ConstructionType.TYPE_IV_A: 216000.0,
    ConstructionType.TYPE_IV_B: 144000.0,
    ConstructionType.TYPE_IV_C: 90000.0,
    ConstructionType.TYPE_IV_HT: 72000.0,
    ConstructionType.TYPE_V_A: 36000.0,
    ConstructionType.TYPE_V_B: 22000.0,
}

_AREA_UTILITY_SM: AreaData = {
    ConstructionType.TYPE_I_A: "UL",
    ConstructionType.TYPE_I_B: 106500.0,
    ConstructionType.TYPE_II_A: 57000.0,
    ConstructionType.TYPE_II_B: 25500.0,
    ConstructionType.TYPE_III_A: 42000.0,
    ConstructionType.TYPE_III_B: 25500.0,
    ConstructionType.TYPE_IV_A: 162000.0,
    ConstructionType.TYPE_IV_B: 108000.0,
    ConstructionType.TYPE_IV_C: 67500.0,
    ConstructionType.TYPE_IV_HT: 54000.0,
    ConstructionType.TYPE_V_A: 27000.0,
    ConstructionType.TYPE_V_B: 16500.0,
}

ALLOWABLE_AREA_BY_OCCUPANCY = {
    Occupancy.GROUP_B: {
        "NS": _AREA_BUSINESS_NS,
        "S1": _AREA_BUSINESS_S1,
        "SM": _AREA_BUSINESS_SM,
    },
    Occupancy.GROUP_E: {
        "NS": _AREA_EDUCATION_NS,
        "S1": _AREA_EDUCATION_S1,
        "SM": _AREA_EDUCATION_SM,
    },
    Occupancy.GROUP_M: {
        "NS": _AREA_MERCANTILE_NS,
        "S1": _AREA_MERCANTILE_S1,
        "SM": _AREA_MERCANTILE_SM,
    },
    Occupancy.GROUP_R_2: {
        "NS": _AREA_RESIDENTIAL_R2_NS,
        "S1": _AREA_RESIDENTIAL_R2_S1,
        "SM": _AREA_RESIDENTIAL_R2_SM,
    },
    Occupancy.GROUP_S_1: {
        "NS": _AREA_STORAGE_S1_NS,
        "S1": _AREA_STORAGE_S1_S1,
        "SM": _AREA_STORAGE_S1_SM,
    },
    Occupancy.GROUP_S_2: {
        "NS": _AREA_STORAGE_S2_NS,
        "S1": _AREA_STORAGE_S2_S1,
        "SM": _AREA_STORAGE_S2_SM,
    },
    Occupancy.GROUP_U: {
        "NS": _AREA_UTILITY_NS,
        "S1": _AREA_UTILITY_S1,
        "SM": _AREA_UTILITY_SM,
    },
}
