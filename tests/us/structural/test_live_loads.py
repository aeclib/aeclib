from aeclib.core import ComplianceStatus
from aeclib.us.structural.live_loads.constants import LiveLoadUse
from aeclib.us.structural.live_loads.generic import get_minimum_live_load, validate_live_load


def test_get_minimum_live_load():
    # Test lookup for Apartments (40 psf, No concentrated) - rerouted to Residential Private
    apt_reqs = get_minimum_live_load(LiveLoadUse.APARTMENTS)
    assert apt_reqs["uniform_psf"] == 40.0
    assert apt_reqs["concentrated_lbs"] is None

    # Test lookup for Office (50 psf, 2000 lbs)
    office_reqs = get_minimum_live_load(LiveLoadUse.OFFICE_OFFICES)
    assert office_reqs["uniform_psf"] == 50.0
    assert office_reqs["concentrated_lbs"] == 2000.0
    assert office_reqs["reduction_permitted"] is True

    # Test lookup for Assembly (Reduction NOT permitted)
    assembly_reqs = get_minimum_live_load(LiveLoadUse.ASSEMBLY_LOBBIES)
    assert assembly_reqs["reduction_permitted"] is False


def test_validate_live_load_pass():
    # Pass scenario for Apartments - rerouted to Residential Private
    result = validate_live_load(
        design_uniform_psf=40.0,
        design_concentrated_lbs=None,
        use=LiveLoadUse.APARTMENTS,
    )
    assert result.status == ComplianceStatus.PASS

    # Pass scenario for Office (Higher than minimum)
    result = validate_live_load(
        design_uniform_psf=60.0,
        design_concentrated_lbs=2500.0,
        use=LiveLoadUse.OFFICE_OFFICES,
    )
    assert result.status == ComplianceStatus.PASS


def test_validate_live_load_fail_uniform():
    # Fail scenario for Apartments - rerouted to Residential Private
    result = validate_live_load(
        design_uniform_psf=30.0,
        design_concentrated_lbs=None,
        use=LiveLoadUse.APARTMENTS,
    )
    assert result.status == ComplianceStatus.FAIL


def test_validate_live_load_fail_concentrated():
    # Fail scenario for Office (Below minimum concentrated)
    result = validate_live_load(
        design_uniform_psf=50.0,
        design_concentrated_lbs=1500.0,
        use=LiveLoadUse.OFFICE_OFFICES,
    )
    assert result.status == ComplianceStatus.FAIL


def test_validate_live_load_missing_concentrated():
    # Fail scenario for Office (Missing required concentrated)
    result = validate_live_load(
        design_uniform_psf=50.0,
        design_concentrated_lbs=None,
        use=LiveLoadUse.OFFICE_OFFICES,
    )
    assert result.status == ComplianceStatus.FAIL


def test_validate_live_load_not_applicable():
    # Helipads reference other sections (no-op in this function)
    result = validate_live_load(
        design_uniform_psf=100.0,
        design_concentrated_lbs=1000.0,
        use=LiveLoadUse.HELIPADS,
    )
    assert result.status == ComplianceStatus.NOT_APPLICABLE


def test_validate_live_load_public_restrooms():
    # Pass scenario for Public Restrooms
    result = validate_live_load(
        design_uniform_psf=60.0,
        design_concentrated_lbs=None,
        use=LiveLoadUse.PUBLIC_RESTROOMS,
    )
    assert result.status == ComplianceStatus.PASS

    # Fail scenario for Public Restrooms
    result = validate_live_load(
        design_uniform_psf=50.0,
        design_concentrated_lbs=None,
        use=LiveLoadUse.PUBLIC_RESTROOMS,
    )
    assert result.status == ComplianceStatus.FAIL
