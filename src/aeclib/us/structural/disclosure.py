import logging
from typing import Any, Optional

from aeclib.core import (
    ComplianceResult,
    ComplianceStatus,
)

logger = logging.getLogger("aeclib")


def validate_floor_live_load_disclosure(
    uniformly_distributed_floor_live_load: Optional[float] = None,
    concentrated_floor_live_load: Optional[float] = None,
    impact_floor_live_load: Optional[float] = None,
    is_live_load_reduction_applied: bool = False,
    **_kwargs: Any,
) -> ComplianceResult:
    """
    Validates disclosure of floor live load data.

    Applicable to:
    - IBC 2024 Section 1603.1.1

    Args:
        uniformly_distributed_floor_live_load: Distributed floor live load (psf).
        concentrated_floor_live_load: Concentrated floor live load (lbs).
        impact_floor_live_load: Impact floor live load (lbs).
        is_live_load_reduction_applied: True if reduction was used.
        **_kwargs: Sink for unused structural facts.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Floor Live Load Disclosure]...")

    missing = []
    if uniformly_distributed_floor_live_load is None:
        missing.append("uniformly_distributed_floor_live_load")
    if concentrated_floor_live_load is None:
        missing.append("concentrated_floor_live_load")
    if impact_floor_live_load is None:
        missing.append("impact_floor_live_load")

    if missing:
        message = (
            f"[FAIL] Missing required floor live load disclosure: {', '.join(missing)}."
        )
        return ComplianceResult(status=ComplianceStatus.FAIL, message=message)

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_roof_live_load_disclosure(
    roof_live_load_psf: Optional[float] = None,
    **_kwargs: Any,
) -> ComplianceResult:
    """
    Validates disclosure of roof live load data.

    Applicable to:
    - IBC 2024 Section 1603.1.2

    Args:
        roof_live_load_psf: Roof live load (psf).
        **_kwargs: Sink for unused structural facts.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Roof Live Load Disclosure]...")

    if roof_live_load_psf is None:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message="[FAIL] roof_live_load_psf must be disclosed.",
        )

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_snow_load_disclosure(
    ground_snow_load_psf: Optional[float] = None,
    flat_roof_snow_load_psf: Optional[float] = None,
    snow_exposure_factor: Optional[float] = None,
    snow_importance_factor: Optional[float] = None,
    snow_thermal_factor: Optional[float] = None,
    snow_drift_factor: Optional[float] = None,
    **_kwargs: Any,
) -> ComplianceResult:
    """
    Validates disclosure of roof snow load data.

    Applicable to:
    - IBC 2024 Section 1603.1.3

    Args:
        ground_snow_load_psf: Ground snow load (psf).
        flat_roof_snow_load_psf: Flat-roof snow load (psf).
        snow_exposure_factor: Snow exposure factor (Ce).
        snow_importance_factor: Snow load importance factor (I).
        snow_thermal_factor: Thermal factor (Ct).
        snow_drift_factor: Drift exposure factor (D).
        **_kwargs: Sink for unused structural facts.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Snow Load Disclosure]...")

    if ground_snow_load_psf is None:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message="[FAIL] ground_snow_load_psf must be disclosed.",
        )

    # Conditional requirement: If Pg > 10 psf, extra data points are required.
    if ground_snow_load_psf > 10.0:
        missing = []
        if flat_roof_snow_load_psf is None:
            missing.append("flat_roof_snow_load_psf")
        if snow_exposure_factor is None:
            missing.append("snow_exposure_factor")
        if snow_importance_factor is None:
            missing.append("snow_importance_factor")
        if snow_thermal_factor is None:
            missing.append("snow_thermal_factor")
        if snow_drift_factor is None:
            missing.append("snow_drift_factor")

        if missing:
            return ComplianceResult(
                status=ComplianceStatus.FAIL,
                message=(
                    f"[FAIL] Ground snow load exceeds 10 psf. "
                    f"Missing required disclosure: {', '.join(missing)}."
                ),
            )

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_wind_design_disclosure(
    basic_wind_speed_mph: Optional[float] = None,
    wind_risk_category: Optional[str] = None,
    wind_exposure_category: Optional[str] = None,
    **_kwargs: Any,
) -> ComplianceResult:
    """
    Validates baseline disclosure of wind design data.

    Applicable to:
    - IBC 2024 Section 1603.1.4

    Args:
        basic_wind_speed_mph: Basic wind speed (mph).
        wind_risk_category: Risk category (e.g., 'I', 'II').
        wind_exposure_category: Wind exposure (e.g., 'B', 'C').
        **_kwargs: Sink for unused structural facts.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Wind Design Disclosure]...")

    missing = []
    if basic_wind_speed_mph is None:
        missing.append("basic_wind_speed_mph")
    if wind_risk_category is None:
        missing.append("wind_risk_category")
    if wind_exposure_category is None:
        missing.append("wind_exposure_category")

    if missing:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f"[FAIL] Missing required wind design disclosure: {', '.join(missing)}."
            ),
        )

    # TODO: Implement complex tornado and component/cladding pressure disclosures.
    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_earthquake_design_disclosure(
    seismic_risk_category: Optional[str] = None,
    seismic_importance_factor: Optional[float] = None,
    seismic_design_category: Optional[str] = None,
    site_class: Optional[str] = None,
    **_kwargs: Any,
) -> ComplianceResult:
    """
    Validates baseline disclosure of earthquake design data.

    Applicable to:
    - IBC 2024 Section 1603.1.5

    Args:
        seismic_risk_category: Risk category.
        seismic_importance_factor: Importance factor (Ie).
        seismic_design_category: Design category (SDC).
        site_class: Soil site class (e.g., 'D').
        **_kwargs: Sink for unused structural facts.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Earthquake Design Disclosure]...")

    missing = []
    if seismic_risk_category is None:
        missing.append("seismic_risk_category")
    if seismic_importance_factor is None:
        missing.append("seismic_importance_factor")
    if seismic_design_category is None:
        missing.append("seismic_design_category")
    if site_class is None:
        missing.append("site_class")

    if missing:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f"[FAIL] Missing required seismic disclosure: {', '.join(missing)}."
            ),
        )

    # TODO: Implement spectral acceleration, shear, and response coefficients.
    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_geotechnical_disclosure(
    design_load_bearing_value_psf: Optional[float] = None,
    **_kwargs: Any,
) -> ComplianceResult:
    """
    Validates disclosure of geotechnical soil data.

    Applicable to:
    - IBC 2024 Section 1603.1.6

    Args:
        design_load_bearing_value_psf: Design load-bearing value of soils (psf).
        **_kwargs: Sink for unused structural facts.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Geotechnical Disclosure]...")

    if design_load_bearing_value_psf is None:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message="[FAIL] design_load_bearing_value_psf must be disclosed.",
        )

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_rain_load_disclosure(
    design_rainfall_intensity_iph: Optional[float] = None,
    is_drainage_shown: bool = False,
    **_kwargs: Any,
) -> ComplianceResult:
    """
    Validates disclosure of roof rain load data.

    Applicable to:
    - IBC 2024 Section 1603.1.9

    Args:
        design_rainfall_intensity_iph: Design rainfall intensity (in/hr).
        is_drainage_shown: True if drain/scupper locations are shown.
        **_kwargs: Sink for unused structural facts.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Rain Load Disclosure]...")

    if design_rainfall_intensity_iph is None:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message="[FAIL] design_rainfall_intensity_iph must be disclosed.",
        )

    if not is_drainage_shown:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message="[FAIL] is_drainage_shown must be True on documents.",
        )

    return ComplianceResult(status=ComplianceStatus.PASS)


def validate_structural_design_disclosure(
    **structural_facts: Any,
) -> ComplianceResult:
    """
    Validates completeness of structural design information in documents.

    Applicable to:
    - IBC 2024 Section 1603.1

    Args:
        **structural_facts: Arbitrary keyword arguments containing structural facts.
                           Expected keys must match aeclib argument names.

    Returns:
        ComplianceResult. (PASS, FAIL, NOT_APPLICABLE)
    """
    logger.info("Checking [Structural Design Disclosure] completeness...")

    # We call our atomic sub-checks. Each check returns a ComplianceResult.
    # Due to the **_kwargs sinks, we can safely pass all facts to every check.
    checks = [
        validate_floor_live_load_disclosure(**structural_facts),
        validate_roof_live_load_disclosure(**structural_facts),
        validate_snow_load_disclosure(**structural_facts),
        validate_wind_design_disclosure(**structural_facts),
        validate_earthquake_design_disclosure(**structural_facts),
        validate_geotechnical_disclosure(**structural_facts),
        validate_rain_load_disclosure(**structural_facts),
    ]

    # Collect all failures
    failures = [r.message for r in checks if not r]

    if failures:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=f"[FAIL] Structural disclosure incomplete: {'; '.join(failures)}",
        )

    # TODO: Add checks for 1603.1.7 (Flood) and 1603.1.8 (Special Loads).
    logger.info("NOTE: [Flood] and [Special Load] disclosures are not yet implemented.")

    return ComplianceResult(status=ComplianceStatus.PASS)
