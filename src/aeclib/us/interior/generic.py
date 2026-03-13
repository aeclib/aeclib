import logging
from typing import Optional, Union

from aeclib.core import (
    ComplianceResult,
    ComplianceStatus,
)
from aeclib.us.common import (
    OccupancyClassification,
)
from aeclib.us.common.dimensions import (
    MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
)

from .constants import ROOM_HEIGHT_THRESHOLDS, RoomType

logger = logging.getLogger("aeclib")


def validate_minimum_ceiling_height(
    ceiling_height_inches: float,
    room_type: Union[str, RoomType] = RoomType.HABITABLE,
    occupancy_classification: Optional[Union[str, OccupancyClassification]] = None,
) -> ComplianceResult:
    """
    Validates general minimum ceiling height requirements.

    Applicable to:
    - IBC 2024 Section 1208.2
    - IBC 2021 Section 1208.2
    - IBC 2018 Section 1208.2

    Args:
        ceiling_height_inches: The measured ceiling height in inches.
        room_type: The functional category of the room.
        occupancy_classification: The occupancy group (e.g., GROUP_R).
        total_area: Total required area of the room (for sloped ceiling checks).
        area_at_required_height: Area within the room meeting the height requirement.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info(f"Checking Section 1208.2 minimum ceiling height for {room_type}...")

    # TODO: Implement Exception 1 (Structural projections/beams).
    # TODO: Implement Exception 2 (Sloped ceilings: 50% area rule and 5' deduction).

    # 1. Determine baseline threshold from RoomType
    threshold = ROOM_HEIGHT_THRESHOLDS.get(
        room_type, ROOM_HEIGHT_THRESHOLDS[RoomType.HABITABLE]
    )

    # 2. Handle Exception 4: Corridors in Group R (Residential)
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
