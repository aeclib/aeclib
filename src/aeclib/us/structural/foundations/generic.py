import logging
from typing import Optional

from aeclib.core import ComplianceResult, ComplianceStatus

from .constants import (
    DEFAULT_ALLOWABLE_BEARING_PRESSURE,
    PRESUMPTIVE_SOIL_VALUES,
    SoilClass,
)

logger = logging.getLogger("aeclib")


def get_allowable_bearing_pressure(soil_class: Optional[SoilClass] = None) -> float:
    """
    Retrieves the allowable foundation bearing pressure (in psf) for a soil classification.

    Applicable to:
    - IBC 2024 Table 1806.2
    - IRC 2024 Table R401.4.1

    Args:
        soil_class: The soil classification from IBC Table 1806.2.
            If None or unknown, the default minimum presumptive value (1500 psf) is used.

    Returns:
        The allowable bearing pressure in psf.
    """
    if soil_class is None:
        return DEFAULT_ALLOWABLE_BEARING_PRESSURE

    if soil_class not in PRESUMPTIVE_SOIL_VALUES:
        raise ValueError(f"Unknown soil class: {soil_class}")

    return PRESUMPTIVE_SOIL_VALUES[soil_class]["allowable_bearing_psf"]


def validate_bearing_pressure(
    design_bearing_pressure: float,
    soil_class: Optional[SoilClass] = None,
) -> ComplianceResult:
    """
    Validates design bearing pressure against allowable presumptive values.

    Applicable to:
    - IBC 2024 Section 1806.2
    - IRC 2024 Section R401.4.1

    Args:
        design_bearing_pressure: The designed bearing pressure in psf.
        soil_class: The classification of the soil/foundation material.
            If None or unknown, the default minimum presumptive value (1500 psf) is used.

    Returns:
        ComplianceResult. (PASS, FAIL)
    """
    if soil_class is None:
        logger.info(
            "Soil classification is unknown/unspecified. "
            f"Defaulting to the minimum allowable bearing pressure of {DEFAULT_ALLOWABLE_BEARING_PRESSURE} psf."
        )
        allowable = DEFAULT_ALLOWABLE_BEARING_PRESSURE
    else:
        logger.info(f"Checking bearing pressure for soil classification: {soil_class}...")
        if soil_class not in PRESUMPTIVE_SOIL_VALUES:
            raise ValueError(f"Unknown soil class: {soil_class}")
        allowable = PRESUMPTIVE_SOIL_VALUES[soil_class]["allowable_bearing_psf"]

    if design_bearing_pressure > allowable:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f"[FAIL] Design bearing pressure {design_bearing_pressure} psf exceeds "
                f"the allowable bearing pressure of {allowable} psf."
            ),
        )

    return ComplianceResult(status=ComplianceStatus.PASS)


def get_presumptive_soil_properties(soil_class: Optional[SoilClass] = None) -> dict:
    """
    Retrieves the presumptive values/properties for a soil classification from IBC Table 1806.2.

    Applicable to:
    - IBC 2024 Table 1806.2

    Args:
        soil_class: The soil classification.
            If None or unknown, returns the values for CLAY_SILTY_CLAY (default/minimum values).

    Returns:
        A dictionary containing soil properties:
        - "allowable_bearing_psf": float
        - "lateral_bearing_psf_per_ft": float
        - "sliding_coefficient": Optional[float]
        - "sliding_cohesion_psf": Optional[float]
    """
    if soil_class is None:
        soil_class = SoilClass.CLAY_SILTY_CLAY

    if soil_class not in PRESUMPTIVE_SOIL_VALUES:
        raise ValueError(f"Unknown soil class: {soil_class}")

    return PRESUMPTIVE_SOIL_VALUES[soil_class].copy()
