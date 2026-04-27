from enum import Enum


class Occupancy(str, Enum):
    """
    Standardized occupancy classifications for building design.

    Applicable to:
    - IBC 2024 Section 302.1
    """

    GROUP_A = "A"  # Assembly Base
    GROUP_A_1 = "A-1"  # Theaters, concert halls (usually with fixed seating)
    GROUP_A_2 = "A-2"  # Restaurants, bars, banquet halls (food and drink consumption)
    GROUP_A_3 = "A-3"  # Places of worship, recreation, libraries, museums
    GROUP_A_4 = "A-4"  # Indoor sporting events, arenas
    GROUP_A_5 = "A-5"  # Outdoor stadiums, bleachers, grandstands

    GROUP_B = "B"  # Business (Offices, banks, outpatient clinics, higher education)

    GROUP_E = "E"  # Educational (K-12 schools, day cares for children > 2.5 yrs)

    GROUP_F = "F"  # Factory Base
    GROUP_F_1 = "F-1"  # Moderate-hazard industrial/manufacturing
    GROUP_F_2 = "F-2"  # Low-hazard industrial/manufacturing

    GROUP_H = "H"  # High Hazard Base
    GROUP_H_1 = "H-1"  # Detonation hazard
    GROUP_H_2 = "H-2"  # Deflagration hazard / Accelerated burning
    GROUP_H_3 = "H-3"  # Physical hazard / Readily support combustion
    GROUP_H_4 = "H-4"  # Health hazard (corrosives, highly toxic materials)
    GROUP_H_5 = "H-5"  # Semiconductor fabrication facilities

    GROUP_I = "I"  # Institutional Base
    GROUP_I_1 = "I-1"  # Assisted living, group homes (>16 persons, 24h care)
    GROUP_I_2 = "I-2"  # Hospitals, nursing homes (incapable of self-preservation)
    GROUP_I_3 = "I-3"  # Prisons, jails, detention centers
    GROUP_I_4 = "I-4"  # Day care facilities (>5 persons, infants or adult care)

    GROUP_M = "M"  # Mercantile (Retail stores, markets, department stores)

    # Residential Base (Note: Standard detached single-family homes are typically IRC)
    GROUP_R = "R"
    GROUP_R_1 = "R-1"  # Transient boarding (Hotels, motels)
    GROUP_R_2 = "R-2"  # Non-transient, multi-dwelling (Apartments, dormitories)
    GROUP_R_3 = "R-3"  # Permanent, small scale (1-2 family dwellings, small care facilities)
    GROUP_R_4 = "R-4"  # Residential care / assisted living (6-16 persons)

    GROUP_S = "S"  # Storage Base
    GROUP_S_1 = "S-1"  # Moderate-hazard storage
    GROUP_S_2 = "S-2"  # Low-hazard storage (Noncombustible materials, parking garages)

    GROUP_U = "U"  # Utility and Miscellaneous (Barns, sheds, fences, retaining walls)


def get_base_classification(occupancy: Occupancy) -> Occupancy:
    """
    Extracts the base classification from a subclassification (e.g., 'A-2' -> 'A').
    """
    base_str = occupancy.value.split("-")[0]
    return Occupancy(base_str)


def is_base_classification(occupancy: Occupancy, base: Occupancy) -> bool:
    """
    Checks if a given occupancy falls under a specific base classification.
    """
    return get_base_classification(occupancy) == base
