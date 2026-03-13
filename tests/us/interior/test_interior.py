import logging

from aeclib.core import ComplianceStatus
from aeclib.us.common import OccupancyClassification
from aeclib.us.interior import RoomType, validate_minimum_ceiling_height

# Configure logging for clearer test output
logging.basicConfig(level=logging.WARNING)


def test_validate_minimum_ceiling_height_standard():
    # Standard: Habitable Room (Default) -> 90"
    result = validate_minimum_ceiling_height(ceiling_height_inches=90.0)
    assert result.status == ComplianceStatus.PASS

    result = validate_minimum_ceiling_height(ceiling_height_inches=84.0)
    assert result.status == ComplianceStatus.FAIL


def test_validate_minimum_ceiling_height_service():
    # Service Area (Kitchen): 84" -> PASS
    result = validate_minimum_ceiling_height(
        ceiling_height_inches=84.0, room_type=RoomType.KITCHEN
    )
    assert result.status == ComplianceStatus.PASS


def test_validate_minimum_ceiling_height_residential_corridor():
    # Exception 4: Corridor in Group R -> 84" (7'0")
    result = validate_minimum_ceiling_height(
        ceiling_height_inches=84.0,
        room_type=RoomType.CORRIDOR,
        occupancy_classification=OccupancyClassification.GROUP_R,
    )
    assert result.status == ComplianceStatus.PASS

    # Standard Corridor (Non-Residential) -> 90" (7'6")
    result = validate_minimum_ceiling_height(
        ceiling_height_inches=84.0,
        room_type=RoomType.CORRIDOR,
        occupancy_classification=OccupancyClassification.GROUP_B,  # Business
    )
    assert result.status == ComplianceStatus.FAIL
