import logging
from typing import Union

from .constants import (
    MAXIMUM_FLOOR_AREA_ALLOWANCES_PER_OCCUPANT,
    AreaBasis,
    SpaceFunction,
)

logger = logging.getLogger("aeclib")


def validate_occupant_load_without_fixed_seating(
    function_type: Union[str, SpaceFunction],
    gross_area: float,
    net_area: float,
    design_occupancy_count: int,
) -> bool:
    """
    Validates design occupancy count against required minimum for
    areas without fixed seating.

    Applicable to:
    - IBC 2024 Section 1004.5
    - IBC 2021 Section 1004.5
    - IBC 2018 Section 1004.5

    Args:
        function_type: The functional category of the space (e.g., 'business').
        gross_area: The gross floor area.
        net_area: The net floor area.
        design_occupancy_count: The intended number of occupants.

    Returns:
        True if compliant, False otherwise.
    """
    rule = MAXIMUM_FLOOR_AREA_ALLOWANCES_PER_OCCUPANT.get(function_type)
    if not rule:
        logger.error(f"Unsupported function type: {function_type}")
        raise ValueError(f"Function type '{function_type}' is not supported.")

    logger.info(f"Checking {function_type} occupancy load factors...")
    logger.info(f"{function_type} occupancy load factors: {rule}")
    factor = rule["factor"]
    basis = rule["basis"]

    # Select the correct area based on the rule's basis
    effective_area = net_area if basis == AreaBasis.NET else gross_area

    # Calculate the required minimum (standard practice rounds down
    # for occupancy load calculations)
    required_min = int(effective_area / factor)

    is_compliant = design_occupancy_count >= required_min

    if not is_compliant:
        logger.warning(
            f"Compliance Fail: Design occupancy ({design_occupancy_count}) "
            f"is less than required minimum of {required_min} for {function_type} "
            f"({basis} area: {effective_area}, factor: {factor})."
        )

    return is_compliant


def validate_increased_occupant_load(area: float, occupant_count: int) -> bool:
    """
    Validates that the occupant load does not exceed the limit for increased loads.

    Applicable to:
    - IBC 2024 Section 1004.5.1
    - IBC 2021 Section 1004.5.1
    - IBC 2018 Section 1004.5.1

    Args:
        area: The occupiable floor space.
        occupant_count: The intended number of occupants.

    Returns:
        True if compliant, False otherwise.
    """
    if occupant_count <= 0:
        return True

    max_density_threshold = 7.0
    max_occupant_count = area / max_density_threshold
    is_compliant = occupant_count <= max_occupant_count

    if not is_compliant:
        logger.warning(
            f"Compliance Fail: Occupant count {occupant_count} "
            f"exceeds limit of {max_occupant_count}"
        )

    return is_compliant
