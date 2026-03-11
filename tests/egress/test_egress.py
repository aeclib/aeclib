import logging

import pytest

from aeclib.common import ComplianceStatus
from aeclib.egress import (
    validate_ceiling_height,
    validate_increased_occupant_load,
    validate_occupant_load_without_fixed_seating,
)

# Configure logging for clearer test output
logging.basicConfig(level=logging.WARNING)


def test_validate_ceiling_height_standard_pass():
    # Standard rule: 7'6" (90") -> PASS
    result = validate_ceiling_height(ceiling_height_inches=90.0)
    assert result.status == ComplianceStatus.PASS
    assert bool(result) is True

    # 8'0" (96") -> PASS
    assert (
        validate_ceiling_height(ceiling_height_inches=96.0).status
        == ComplianceStatus.PASS
    )


def test_validate_ceiling_height_standard_fail():
    # 7'0" (84") -> FAIL
    result = validate_ceiling_height(ceiling_height_inches=84.0)
    assert result.status == ComplianceStatus.FAIL
    assert "is less than required minimum" in result.message
    assert bool(result) is False

    # 7'5.9" (89.9") -> FAIL
    assert (
        validate_ceiling_height(ceiling_height_inches=89.9).status
        == ComplianceStatus.FAIL
    )


def test_validate_ceiling_height_not_applicable():
    # Negative height -> NOT_APPLICABLE
    result = validate_ceiling_height(ceiling_height_inches=-1.0)
    assert result.status == ComplianceStatus.NOT_APPLICABLE


def test_validate_occupant_load_business_gross():
    # Business: 1500 Gross, 1200 Net. Factor is 150 Gross.
    # Required: 1500 / 150 = 10.
    # Case A: Declared 12 -> PASS
    result = validate_occupant_load_without_fixed_seating(
        function_type="business",
        gross_area=1500.0,
        net_area=1200.0,
        design_occupancy_count=12,
    )
    assert result.status == ComplianceStatus.PASS
    assert bool(result) is True


def test_validate_occupant_load_classroom_net():
    # Classroom: 1000 Gross, 800 Net. Factor is 20 Net.
    # Required: 800 / 20 = 40.
    # Case B: Declared 35 -> FAIL
    result = validate_occupant_load_without_fixed_seating(
        function_type="educational_classroom",
        gross_area=1000.0,
        net_area=800.0,
        design_occupancy_count=35,
    )
    assert result.status == ComplianceStatus.FAIL
    assert bool(result) is False


def test_validate_increased_occupant_load():
    # Density check: 1000 sqft / 200 people = 5 sqft/person (Limit 7) -> FAIL
    result = validate_increased_occupant_load(area=1000, occupant_count=200)
    assert result.status == ComplianceStatus.FAIL
    assert bool(result) is False


def test_invalid_function_type():
    # Test that an unsupported function type raises a ValueError
    with pytest.raises(ValueError, match="is not supported"):
        validate_occupant_load_without_fixed_seating(
            function_type="non_existent_function_type",
            gross_area=1000,
            net_area=800,
            design_occupancy_count=10,
        )


def test_zero_occupancy_is_always_compliant():
    # 1004.5.1: If there are no people, there is no density issue.
    assert (
        validate_increased_occupant_load(area=1000, occupant_count=0).status
        == ComplianceStatus.PASS
    )
    assert (
        validate_increased_occupant_load(area=1000, occupant_count=-1).status
        == ComplianceStatus.PASS
    )
