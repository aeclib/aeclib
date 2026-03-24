from aeclib.core import ComplianceStatus
from aeclib.us.structural import (
    validate_earthquake_design_disclosure,
    validate_floor_live_load_disclosure,
    validate_geotechnical_disclosure,
    validate_rain_load_disclosure,
    validate_roof_live_load_disclosure,
    validate_snow_load_disclosure,
    validate_structural_design_disclosure,
    validate_wind_design_disclosure,
)


def test_validate_floor_live_load_disclosure():
    # [Floor Live Load Disclosure]: Missing concentrated load -> FAIL
    assert (
        validate_floor_live_load_disclosure(
            uniformly_distributed_floor_live_load=50.0
        ).status
        == ComplianceStatus.FAIL
    )

    # [Floor Live Load Disclosure]: All present -> PASS
    assert (
        validate_floor_live_load_disclosure(
            uniformly_distributed_floor_live_load=50.0,
            concentrated_floor_live_load=2000.0,
            impact_floor_live_load=0.0,
        ).status
        == ComplianceStatus.PASS
    )


def test_validate_roof_live_load_disclosure():
    # [Roof Live Load Disclosure]: Missing -> FAIL
    assert (
        validate_roof_live_load_disclosure(roof_live_load_psf=None).status
        == ComplianceStatus.FAIL
    )
    # [Roof Live Load Disclosure]: Present -> PASS
    assert (
        validate_roof_live_load_disclosure(roof_live_load_psf=20.0).status
        == ComplianceStatus.PASS
    )


def test_validate_snow_load_disclosure():
    # [Snow Load Disclosure]: ground_snow_load_psf missing -> FAIL
    assert (
        validate_snow_load_disclosure(ground_snow_load_psf=None).status
        == ComplianceStatus.FAIL
    )
    # [Snow Load Disclosure]: Low snow -> PASS
    assert (
        validate_snow_load_disclosure(ground_snow_load_psf=5.0).status
        == ComplianceStatus.PASS
    )


def test_validate_wind_design_disclosure():
    # [Wind Disclosure]: Missing speed -> FAIL
    assert (
        validate_wind_design_disclosure(wind_risk_category="II").status
        == ComplianceStatus.FAIL
    )
    # [Wind Disclosure]: All present -> PASS
    assert (
        validate_wind_design_disclosure(
            basic_wind_speed_mph=115.0,
            wind_risk_category="II",
            wind_exposure_category="B",
        ).status
        == ComplianceStatus.PASS
    )


def test_validate_earthquake_design_disclosure():
    # [Seismic Disclosure]: All present -> PASS
    assert (
        validate_earthquake_design_disclosure(
            seismic_risk_category="II",
            seismic_importance_factor=1.0,
            seismic_design_category="D",
            site_class="D",
        ).status
        == ComplianceStatus.PASS
    )


def test_validate_geotechnical_disclosure():
    # [Geotech Disclosure]: All present -> PASS
    assert (
        validate_geotechnical_disclosure(design_load_bearing_value_psf=1500.0).status
        == ComplianceStatus.PASS
    )


def test_validate_rain_load_disclosure():
    # [Rain Disclosure]: Missing drainage info -> FAIL
    assert (
        validate_rain_load_disclosure(
            design_rainfall_intensity_iph=2.0, is_drainage_shown=False
        ).status
        == ComplianceStatus.FAIL
    )


def test_validate_structural_design_disclosure_aggregate():
    # [Aggregate Disclosure]: Full set of clean data -> PASS
    full_data = {
        "uniformly_distributed_floor_live_load": 50.0,
        "concentrated_floor_live_load": 2000.0,
        "impact_floor_live_load": 0.0,
        "roof_live_load_psf": 20.0,
        "ground_snow_load_psf": 5.0,
        "basic_wind_speed_mph": 115.0,
        "wind_risk_category": "II",
        "wind_exposure_category": "B",
        "seismic_risk_category": "II",
        "seismic_importance_factor": 1.0,
        "seismic_design_category": "D",
        "site_class": "D",
        "design_load_bearing_value_psf": 1500.0,
        "design_rainfall_intensity_iph": 3.0,
        "is_drainage_shown": True,
    }

    result = validate_structural_design_disclosure(**full_data)
    assert result.status == ComplianceStatus.PASS


def test_validate_structural_design_disclosure_incomplete():
    # [Aggregate Disclosure]: Missing one required field (geotech) -> FAIL
    incomplete_data = {
        "uniformly_distributed_floor_live_load": 50.0,
        "concentrated_floor_live_load": 2000.0,
        "impact_floor_live_load": 0.0,
        "roof_live_load_psf": 20.0,
        "ground_snow_load_psf": 5.0,
        # geotechnical is missing
    }

    result = validate_structural_design_disclosure(**incomplete_data)
    assert result.status == ComplianceStatus.FAIL
    assert "design_load_bearing_value_psf" in result.message
