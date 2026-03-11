import logging
from typing import Union

from aeclib.common import ComplianceResult, ComplianceStatus
from aeclib.common.dimensions import MINIMUM_CEILING_HEIGHT_STANDARD_INCHES

from .constants import (
    MAXIMUM_FLOOR_AREA_ALLOWANCES_PER_OCCUPANT,
    AreaBasis,
    SpaceFunction,
)

logger = logging.getLogger("aeclib")


def validate_ceiling_height(ceiling_height_inches: float) -> ComplianceResult:
    """
    Validates that the ceiling height meets the minimum requirement
    for the means of egress.

    Applicable to:
    - IBC 2024 Section 1003.2
    - IBC 2021 Section 1003.2
    - IBC 2018 Section 1003.2

    Args:
        ceiling_height_inches: The measured ceiling height in inches.

    Returns:
        ComplianceResult object with PASS, FAIL, or NOT_APPLICABLE status.
    """
    logger.info(f"Checking ceiling height: {ceiling_height_inches} inches...")

    if ceiling_height_inches < 0:
        return ComplianceResult(
            status=ComplianceStatus.NOT_APPLICABLE,
            message="Measured height is negative; check source data.",
        )

    is_compliant = ceiling_height_inches >= MINIMUM_CEILING_HEIGHT_STANDARD_INCHES

    if not is_compliant:
        message = (
            f'[FAIL] Ceiling height ({ceiling_height_inches}") is less than '
            f'required minimum of {MINIMUM_CEILING_HEIGHT_STANDARD_INCHES}".'
        )
        return ComplianceResult(status=ComplianceStatus.FAIL, message=message)

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_occupant_load_without_fixed_seating(
    function_type: Union[str, SpaceFunction],
    gross_area: float,
    net_area: float,
    design_occupancy_count: int,
) -> ComplianceResult:
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
        ComplianceResult object with PASS, FAIL, or NOT_APPLICABLE status.
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
        message = (
            f"[FAIL] Design occupancy ({design_occupancy_count}) is less than "
            f"required minimum of {required_min} for {function_type} "
            f"({basis} area: {effective_area}, factor: {factor})."
        )
        return ComplianceResult(status=ComplianceStatus.FAIL, message=message)

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_increased_occupant_load(
    area: float, occupant_count: int
) -> ComplianceResult:
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
        ComplianceResult object with PASS, FAIL, or NOT_APPLICABLE status.
    """
    if occupant_count <= 0:
        return ComplianceResult(status=ComplianceStatus.PASS)

    max_density_threshold = 7.0
    max_occupant_count = area / max_density_threshold
    is_compliant = occupant_count <= max_occupant_count

    if not is_compliant:
        message = (
            f"[FAIL] Occupant count {occupant_count} "
            f"exceeds limit of {max_occupant_count:.2f} (1 person per 7 sqft)."
        )
        return ComplianceResult(status=ComplianceStatus.FAIL, message=message)

    return ComplianceResult(status=ComplianceStatus.PASS)
