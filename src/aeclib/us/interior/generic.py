import logging
from typing import Optional, Union

from aeclib.core import (
    ComplianceResult,
    ComplianceStatus,
    RoomType,
)
from aeclib.us.common import (
    OccupancyClassification,
)
from aeclib.us.common.dimensions import (
    MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
    MINIMUM_CEILING_HEIGHT_STANDARD_INCHES,
)

from .constants import ROOM_HEIGHT_THRESHOLDS

logger = logging.getLogger("aeclib")


def validate_minimum_ceiling_height(
    ceiling_height_inches: float,
    room_type: Optional[Union[str, RoomType]] = None,
    occupancy_classification: Optional[Union[str, OccupancyClassification]] = None,
) -> ComplianceResult:
    """
    Validates general minimum ceiling height requirements.

    Applicable to:
    - IBC 2024 Section 1208.2

    Args:
        ceiling_height_inches: The measured ceiling height in inches.
        room_type: The functional category of the room (None = Standard space).
        occupancy_classification: The occupancy group (e.g., GROUP_R).

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info(f"Checking Section 1208.2 minimum ceiling height for {room_type}...")

    # Explicit Out-of-Scope handling
    if room_type in {RoomType.ATTIC, RoomType.CRAWL_SPACE}:
        message = (
            f"[NOT_APPLICABLE] Minimum ceiling height standards "
            f"do not apply to {room_type}."
        )
        return ComplianceResult(status=ComplianceStatus.NOT_APPLICABLE, message=message)

    # TODO: Implement [Structural Projections/Beams] exception.
    logger.info(
        "NOTE: [Structural Projections/Beams] exception is not currently considered."
    )

    # TODO: Implement [Sloped Ceilings] exception (50% area rule and 5' deduction).
    logger.info("NOTE: [Sloped Ceilings] exception is not currently considered.")

    # TODO: Implement [Furred Ceilings] rule (2/3 area rule and 7' absolute min).
    logger.info("NOTE: [Furred Ceilings] rule is not currently considered.")

    # 1. Determine baseline threshold
    # Default to 90" (Habitable/Occupiable baseline) unless specifically mapped
    threshold = ROOM_HEIGHT_THRESHOLDS.get(
        room_type, MINIMUM_CEILING_HEIGHT_STANDARD_INCHES
    )

    # 2. Handle [Residential Unit Corridor] exception
    # Reduced to 7' 0" (84")
    if (
        room_type == RoomType.CORRIDOR
        and occupancy_classification == OccupancyClassification.GROUP_R
    ):
        threshold = MINIMUM_CEILING_HEIGHT_SERVICE_INCHES

    # 3. Standard height check
    if ceiling_height_inches < threshold:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f'[FAIL] Ceiling height {ceiling_height_inches}" '
                f'is below the {threshold}" minimum for {room_type}.'
            ),
        )

    return ComplianceResult(status=ComplianceStatus.PASS)
