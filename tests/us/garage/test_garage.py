from aeclib.core import ComplianceStatus
from aeclib.us.garage import validate_garage_clear_height


def test_validate_garage_clear_height():
    # [Parking Garage Clearance]: 7'0" (84") -> PASS
    assert validate_garage_clear_height(84.0).status == ComplianceStatus.PASS
    # 8'0" -> PASS
    assert validate_garage_clear_height(96.0).status == ComplianceStatus.PASS
    # 6'8" (80") -> FAIL
    result = validate_garage_clear_height(80.0)
    assert result.status == ComplianceStatus.FAIL
