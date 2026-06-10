import pytest

from aeclib.core import ComplianceStatus
from aeclib.us.structural.foundations import (
    DEFAULT_ALLOWABLE_BEARING_PRESSURE,
    SoilClass,
    get_allowable_bearing_pressure,
    get_presumptive_soil_properties,
    validate_bearing_pressure,
)


def test_get_allowable_bearing_pressure():
    # Test default (unknown soil)
    assert get_allowable_bearing_pressure() == DEFAULT_ALLOWABLE_BEARING_PRESSURE
    assert get_allowable_bearing_pressure(None) == DEFAULT_ALLOWABLE_BEARING_PRESSURE

    # Test specific soil classes
    assert get_allowable_bearing_pressure(SoilClass.CRYSTALLINE_BEDROCK) == 12000.0
    assert get_allowable_bearing_pressure(SoilClass.SAND_SILTY_SAND) == 2000.0
    assert get_allowable_bearing_pressure(SoilClass.CLAY_SILTY_CLAY) == 1500.0

    # Test invalid soil class
    with pytest.raises(ValueError, match="Unknown soil class"):
        get_allowable_bearing_pressure("invalid_soil_class")


def test_validate_bearing_pressure_default():
    # Pass scenario (below default 1500.0 psf)
    result = validate_bearing_pressure(design_bearing_pressure=1000.0)
    assert result.status == ComplianceStatus.PASS
    assert bool(result) is True

    # Limit case (exactly equal to default 1500.0 psf)
    result = validate_bearing_pressure(design_bearing_pressure=1500.0)
    assert result.status == ComplianceStatus.PASS

    # Fail scenario (above default 1500.0 psf)
    result = validate_bearing_pressure(design_bearing_pressure=1600.0)
    assert result.status == ComplianceStatus.FAIL
    assert bool(result) is False
    assert "exceeds" in result.message


def test_validate_bearing_pressure_specific():
    # Pass scenario (below allowable 3000.0 psf for gravel)
    result = validate_bearing_pressure(design_bearing_pressure=2500.0, soil_class=SoilClass.SANDY_GRAVEL_GRAVEL)
    assert result.status == ComplianceStatus.PASS

    # Fail scenario (above allowable 3000.0 psf for gravel)
    result = validate_bearing_pressure(design_bearing_pressure=3500.0, soil_class=SoilClass.SANDY_GRAVEL_GRAVEL)
    assert result.status == ComplianceStatus.FAIL

    # Test invalid soil class
    with pytest.raises(ValueError, match="Unknown soil class"):
        validate_bearing_pressure(design_bearing_pressure=1000.0, soil_class="invalid")


def test_get_presumptive_soil_properties():
    # Test default
    default_props = get_presumptive_soil_properties()
    assert default_props["allowable_bearing_psf"] == 1500.0
    assert default_props["lateral_bearing_psf_per_ft"] == 100.0
    assert default_props["sliding_coefficient"] is None
    assert default_props["sliding_cohesion_psf"] == 130.0

    # Test specific class
    rock_props = get_presumptive_soil_properties(SoilClass.SEDIMENTARY_FOLIATED_ROCK)
    assert rock_props["allowable_bearing_psf"] == 4000.0
    assert rock_props["lateral_bearing_psf_per_ft"] == 400.0
    assert rock_props["sliding_coefficient"] == 0.35
    assert rock_props["sliding_cohesion_psf"] is None

    # Test invalid class
    with pytest.raises(ValueError, match="Unknown soil class"):
        get_presumptive_soil_properties("invalid_soil_class")
