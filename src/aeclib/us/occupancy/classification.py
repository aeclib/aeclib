from aeclib.us.common.occupancy import Occupancy


def determine_assembly_classification(occupant_load: int, area: float, is_accessory: bool) -> Occupancy:
    """
    Determines if an assembly space can be downgraded to Business.

    Applicable to:
    - IBC 2024 Section 303.1.1
    - IBC 2024 Section 303.1.2

    Args:
        occupant_load: The number of occupants in the assembly space.
        area: The area of the assembly space in square feet.
        is_accessory: Whether the assembly space is accessory to another occupancy.

    Returns:
        Occupancy.
    """
    if is_accessory and occupant_load < 50:
        return Occupancy.GROUP_B
    if is_accessory and area < 750.0:
        return Occupancy.GROUP_B

    return Occupancy.GROUP_A


def determine_care_classification(occupant_count: int, age_under_2_5: bool, is_24_hour_care: bool) -> Occupancy:
    """
    Determines the Institutional, Educational, or Residential classification for care facilities.

    Applicable to:
    - IBC 2024 Section 305
    - IBC 2024 Section 308

    Args:
        occupant_count: The number of persons receiving care.
        age_under_2_5: Whether the persons receiving care are under 2.5 years of age.
        is_24_hour_care: Whether care is provided on a 24-hour basis.

    Returns:
        Occupancy.
    """
    if age_under_2_5:
        if occupant_count > 5:
            return Occupancy.GROUP_I_4
        else:
            return Occupancy.GROUP_R_3

    if is_24_hour_care:
        if occupant_count > 16:
            return Occupancy.GROUP_I_1
        elif occupant_count >= 6:
            return Occupancy.GROUP_R_4
        else:
            return Occupancy.GROUP_R_3

    # Default to E for educational/daycare of older children without 24-hour care
    return Occupancy.GROUP_E


def determine_residential_classification(is_transient: bool, occupant_count: int) -> Occupancy:
    """
    Determines Residential classification for congregate living facilities.

    Applicable to:
    - IBC 2024 Section 310

    Args:
        is_transient: Whether the occupants are transient (e.g., hotel/motel).
        occupant_count: The number of occupants in the facility.

    Returns:
        Occupancy.
    """
    if is_transient:
        if occupant_count <= 10:
            return Occupancy.GROUP_R_3
        else:
            return Occupancy.GROUP_R_1
    else:
        if occupant_count > 16:
            return Occupancy.GROUP_R_2
        else:
            return Occupancy.GROUP_R_3
