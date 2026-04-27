import logging
from typing import Optional, Union

from aeclib.core import (
    ComplianceResult,
    ComplianceStatus,
    RoomType,
)
from aeclib.us.common import (
    Occupancy,
    is_base_classification,
)
from aeclib.us.common.dimensions import (
    MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
    MINIMUM_CEILING_HEIGHT_STANDARD_INCHES,
    MINIMUM_HABITABLE_ROOM_WIDTH_INCHES,
    MINIMUM_KITCHEN_PASSAGEWAY_INCHES,
)

from .constants import ROOM_HEIGHT_THRESHOLDS

logger = logging.getLogger("aeclib")


def validate_minimum_room_width(
    width_inches: Union[float, list[float]],
    room_type: Optional[Union[str, RoomType]] = None,
) -> ComplianceResult:
    """
    Validates minimum room width and kitchen passageways.

    Applicable to:
    - IBC 2024 Section 1208.1

    Args:
        width_inches: One or more measured plan dimensions or clear passageway widths.
        room_type: The functional category of the room.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info(f"Checking minimum room width for {room_type}...")

    # Normalize input to a list for uniform processing
    dimensions = [width_inches] if isinstance(width_inches, (int, float)) else width_inches

    # 1. Handle [Non-Habitable / Service] spaces (NOT_APPLICABLE)
    # These areas (storage, laundry, bathrooms, mechanical, etc.)
    # are not subject to the 7' minimum habitable width rule.
    non_habitable_types = {
        RoomType.BATHROOM,
        RoomType.STORAGE_ROOM,
        RoomType.LAUNDRY_ROOM,
        RoomType.ATTIC,
        RoomType.CRAWL_SPACE,
        RoomType.MECHANICAL_ROOM,
        RoomType.PARKING_GARAGE,
        RoomType.CORRIDOR,
    }

    if room_type in non_habitable_types:
        if room_type == RoomType.BATHROOM:
            logger.info("NOTE: Bathroom dimensions are governed by fixture clearance and accessibility standards.")

        return ComplianceResult(
            status=ComplianceStatus.NOT_APPLICABLE,
            message=(
                f"[NOT_APPLICABLE] Room type '{room_type}' is non-habitable and "
                "is not subject to minimum room width requirements."
            ),
        )

    # 2. Determine Threshold
    if room_type == RoomType.KITCHEN:
        threshold = MINIMUM_KITCHEN_PASSAGEWAY_INCHES
        label = "Kitchen clear passageway"
    else:
        # Default for all other habitable spaces (or non-specified rooms)
        threshold = MINIMUM_HABITABLE_ROOM_WIDTH_INCHES
        label = "Habitable space dimension"

    # 3. Validate all dimensions
    for dim in dimensions:
        if dim < threshold:
            return ComplianceResult(
                status=ComplianceStatus.FAIL,
                message=(f'[FAIL] {label} of {dim}" is less than the minimum required {threshold}".'),
            )

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_minimum_ceiling_height(
    ceiling_height_inches: float,
    room_type: Optional[RoomType] = None,
    occupancy: Optional[Occupancy] = None,
) -> ComplianceResult:
    """
    Validates general minimum ceiling height requirements.

    Applicable to:
    - IBC 2024 Section 1208.2

    Args:
        ceiling_height_inches: The measured ceiling height in inches.
        room_type: The functional category of the room (None = Standard space).
        occupancy: The occupancy group (e.g., GROUP_R).

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info(f"Checking minimum ceiling height for {room_type}...")

    # Explicit Out-of-Scope handling
    if room_type in {RoomType.ATTIC, RoomType.CRAWL_SPACE}:
        message = f"[NOT_APPLICABLE] Minimum ceiling height standards do not apply to {room_type}."
        return ComplianceResult(status=ComplianceStatus.NOT_APPLICABLE, message=message)

    # TODO: Implement [Structural Projections/Beams] exception.
    logger.info("NOTE: [Structural Projections/Beams] exception is not currently considered.")

    # TODO: Implement [Sloped Ceilings] exception (50% area rule and 5' deduction).
    logger.info("NOTE: [Sloped Ceilings] exception is not currently considered.")

    # TODO: Implement [Furred Ceilings] rule (2/3 area rule and 7' absolute min).
    logger.info("NOTE: [Furred Ceilings] rule is not currently considered.")

    # 1. Determine baseline threshold
    # Default to 90" (Habitable/Occupiable baseline) unless specifically mapped
    threshold = ROOM_HEIGHT_THRESHOLDS.get(room_type, MINIMUM_CEILING_HEIGHT_STANDARD_INCHES)

    # 2. Handle [Residential Unit Corridor] exception
    # Reduced to 7' 0" (84")
    if room_type == RoomType.CORRIDOR and occupancy and is_base_classification(occupancy, Occupancy.GROUP_R):
        threshold = MINIMUM_CEILING_HEIGHT_SERVICE_INCHES

    # 3. Standard height check
    if ceiling_height_inches < threshold:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f'[FAIL] Ceiling height {ceiling_height_inches}" is below the {threshold}" minimum for {room_type}.'
            ),
        )

    return ComplianceResult(status=ComplianceStatus.PASS)
