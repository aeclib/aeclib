import logging

import pytest

from aeclib.occupancy import (
    validate_increased_occupant_load,
    validate_occupant_load_without_fixed_seating,
)

# Configure logging for clearer test output
logging.basicConfig(level=logging.WARNING)


def test_validate_occupant_load_business_gross():
    # Business: 1500 Gross, 1200 Net. Factor is 150 Gross.
    # Required: 1500 / 150 = 10.
    # Case A: Declared 12 -> PASS
    assert (
        validate_occupant_load_without_fixed_seating(
            function_type="business",
            gross_area=1500.0,
            net_area=1200.0,
            design_occupancy_count=12,
        )
        is True
    )


def test_validate_occupant_load_classroom_net():
    # Classroom: 1000 Gross, 800 Net. Factor is 20 Net.
    # Required: 800 / 20 = 40.
    # Case B: Declared 35 -> FAIL
    assert (
        validate_occupant_load_without_fixed_seating(
            function_type="educational_classroom",
            gross_area=1000.0,
            net_area=800.0,
            design_occupancy_count=35,
        )
        is False
    )


def test_validate_increased_occupant_load():
    # Density check: 1000 sqft / 200 people = 5 sqft/person (Limit 7) -> FAIL
    assert validate_increased_occupant_load(area=1000, occupant_count=200) is False


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
    assert validate_increased_occupant_load(area=1000, occupant_count=0) is True
    assert validate_increased_occupant_load(area=1000, occupant_count=-1) is True
