import logging

from aeclib.core import ComplianceStatus, RoomType
from aeclib.us.common import Occupancy
from aeclib.us.interior.generic import (
    validate_minimum_ceiling_height,
    validate_minimum_room_width,
)


def test_validate_minimum_room_width_pass():
    # Pass scenario for Habitable Space (>= 7')
    result = validate_minimum_room_width(width_inches=84.0)
    assert result.status == ComplianceStatus.PASS

    # Pass scenario for Kitchen (>= 3')
    result = validate_minimum_room_width(width_inches=36.0, room_type=RoomType.KITCHEN)
    assert result.status == ComplianceStatus.PASS


def test_validate_minimum_room_width_fail():
    # Fail scenario for Habitable Space (< 7')
    result = validate_minimum_room_width(width_inches=80.0)
    assert result.status == ComplianceStatus.FAIL

    # Fail scenario for Kitchen (< 3')
    result = validate_minimum_room_width(width_inches=30.0, room_type=RoomType.KITCHEN)
    assert result.status == ComplianceStatus.FAIL


def test_validate_minimum_room_width_multi():
    # Pass scenario for standard rectangular room (8' x 10')
    result = validate_minimum_room_width(width_inches=[96.0, 120.0])
    assert result.status == ComplianceStatus.PASS

    # Fail scenario for narrow rectangular room (6' x 15')
    result = validate_minimum_room_width(width_inches=[72.0, 180.0])
    assert result.status == ComplianceStatus.FAIL


def test_validate_minimum_room_width_not_applicable():
    # Not Applicable for non-habitable rooms (e.g., Bathroom)
    result = validate_minimum_room_width(width_inches=30.0, room_type=RoomType.BATHROOM)
    assert result.status == ComplianceStatus.NOT_APPLICABLE


# Configure logging for clearer test output
logging.basicConfig(level=logging.WARNING)


def test_validate_minimum_ceiling_height_standard():
    # [Standard Height]: General Habitable Room (None) -> 90" (7'6")
    result = validate_minimum_ceiling_height(ceiling_height_inches=90.0)
    assert result.status == ComplianceStatus.PASS

    result = validate_minimum_ceiling_height(ceiling_height_inches=84.0)
    assert result.status == ComplianceStatus.FAIL


def test_validate_minimum_ceiling_height_service():
    # [Service Area Height]: Kitchen -> 84" (7'0")
    result = validate_minimum_ceiling_height(ceiling_height_inches=84.0, room_type=RoomType.KITCHEN)
    assert result.status == ComplianceStatus.PASS


def test_validate_minimum_ceiling_height_residential_unit_corridor():
    # [Residential Unit Corridor]: Corridor in Group R -> 84" (7'0")
    result = validate_minimum_ceiling_height(
        ceiling_height_inches=84.0,
        room_type=RoomType.CORRIDOR,
        occupancy=Occupancy.GROUP_R,
    )
    assert result.status == ComplianceStatus.PASS

    # Standard Corridor (Non-Residential) -> 90" (7'6")
    result = validate_minimum_ceiling_height(
        ceiling_height_inches=84.0,
        room_type=RoomType.CORRIDOR,
        occupancy=Occupancy.GROUP_B,
    )
    assert result.status == ComplianceStatus.FAIL


def test_validate_minimum_ceiling_height_mezzanine():
    # [Mezzanine Height]: Mezzanines and spaces below -> 84" (7'0")
    assert (
        validate_minimum_ceiling_height(ceiling_height_inches=84.0, room_type=RoomType.MEZZANINE).status
        == ComplianceStatus.PASS
    )

    assert (
        validate_minimum_ceiling_height(ceiling_height_inches=84.0, room_type=RoomType.BELOW_MEZZANINE).status
        == ComplianceStatus.PASS
    )


def test_validate_minimum_ceiling_height_out_of_scope():
    # [Out-of-Scope]: Attic is not subject to general habitability height standards.
    result = validate_minimum_ceiling_height(ceiling_height_inches=48.0, room_type=RoomType.ATTIC)
    assert result.status == ComplianceStatus.NOT_APPLICABLE
