import logging

from aeclib.core import ComplianceResult, ComplianceStatus
from aeclib.us.common.dimensions import MINIMUM_CEILING_HEIGHT_SERVICE_INCHES

logger = logging.getLogger("aeclib")


def validate_garage_clear_height(
    clear_height_inches: float,
) -> ComplianceResult:
    """
    Validates clear height for vehicle and pedestrian areas in parking garages.

    Applicable to:
    - IBC 2024 Section 406.2.2

    Args:
        clear_height_inches: The measured clear height in inches.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking Section 406.2.2 parking garage clear height...")

    # Standard requirement: 7 feet 0 inches (84")
    threshold = MINIMUM_CEILING_HEIGHT_SERVICE_INCHES

    if clear_height_inches < threshold:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f'[FAIL] Garage clear height {clear_height_inches}" is below '
                f'the {threshold}" minimum required for vehicle/pedestrian areas.'
            ),
        )

    return ComplianceResult(status=ComplianceStatus.PASS)
