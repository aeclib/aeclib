from enum import Enum


class SoilClass(str, Enum):
    """
    Presumptive soil/material classifications.
    Based on IBC 2024 Table 1806.2 / IRC 2024 Table R401.4.1.
    """

    CRYSTALLINE_BEDROCK = "crystalline_bedrock"
    SEDIMENTARY_FOLIATED_ROCK = "sedimentary_foliated_rock"
    SANDY_GRAVEL_GRAVEL = "sandy_gravel_gravel"
    SAND_SILTY_SAND = "sand_silty_sand"
    CLAY_SILTY_CLAY = "clay_silty_clay"


DEFAULT_ALLOWABLE_BEARING_PRESSURE = 1500.0

# Mapping of SoilClass to presumptive soil properties
# Based on IBC Table 1806.2
PRESUMPTIVE_SOIL_VALUES = {
    SoilClass.CRYSTALLINE_BEDROCK: {
        "allowable_bearing_psf": 12000.0,
        "lateral_bearing_psf_per_ft": 1200.0,
        "sliding_coefficient": 0.70,
        "sliding_cohesion_psf": None,
    },
    SoilClass.SEDIMENTARY_FOLIATED_ROCK: {
        "allowable_bearing_psf": 4000.0,
        "lateral_bearing_psf_per_ft": 400.0,
        "sliding_coefficient": 0.35,
        "sliding_cohesion_psf": None,
    },
    SoilClass.SANDY_GRAVEL_GRAVEL: {
        "allowable_bearing_psf": 3000.0,
        "lateral_bearing_psf_per_ft": 200.0,
        "sliding_coefficient": 0.35,
        "sliding_cohesion_psf": None,
    },
    SoilClass.SAND_SILTY_SAND: {
        "allowable_bearing_psf": 2000.0,
        "lateral_bearing_psf_per_ft": 150.0,
        "sliding_coefficient": 0.25,
        "sliding_cohesion_psf": None,
    },
    SoilClass.CLAY_SILTY_CLAY: {
        "allowable_bearing_psf": 1500.0,
        "lateral_bearing_psf_per_ft": 100.0,
        "sliding_coefficient": None,
        "sliding_cohesion_psf": 130.0,
    },
}
