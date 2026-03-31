import logging
from typing import Optional

from aeclib.core import ComplianceResult, ComplianceStatus

from .constants import (
    LIVE_LOAD_REDUCTION_PROHIBITED,
    MINIMUM_LIVE_LOADS,
    LiveLoadUse,
)

logger = logging.getLogger("aeclib")


def get_minimum_live_load(use: LiveLoadUse) -> dict:
    """
    Retrieves the required uniform and concentrated live loads for a given use.

    Args:
        use: The category from IBC Table 1607.1.

    Returns:
        A dictionary with "uniform_psf", "concentrated_lbs", and "reduction_permitted" keys.
    """
    # Handle Alias Rerouting
    if use in {LiveLoadUse.APARTMENTS, LiveLoadUse.HOTELS}:
        use = LiveLoadUse.RESIDENTIAL_HOTELS_MULTIFAMILY_PRIVATE

    result = MINIMUM_LIVE_LOADS.get(use, {"uniform_psf": 0.0, "concentrated_lbs": None})

    # Add reduction metadata
    result["reduction_permitted"] = use not in LIVE_LOAD_REDUCTION_PROHIBITED

    return result


def validate_live_load(
    design_uniform_psf: float,
    design_concentrated_lbs: Optional[float],
    use: LiveLoadUse,
) -> ComplianceResult:
    """
    Validates design live loads against minimum requirements of IBC Table 1607.1.

    Applicable to:
    - IBC 2024 Section 1607.1

    Args:
        design_uniform_psf: The designed uniform live load in psf.
        design_concentrated_lbs: The designed concentrated live load in lbs (None if N/A).
        use: The category from IBC Table 1607.1.

    Returns:
        ComplianceResult. (PASS, FAIL)
    """
    logger.info(f"Checking IBC Section 1607.1 live loads for {use}...")

    # 1. Handle Alias Rerouting
    # 'Apartments' and 'Hotels' are shorthand for Residential 'Private' areas.
    if use in {LiveLoadUse.APARTMENTS, LiveLoadUse.HOTELS}:
        original_use = use
        use = LiveLoadUse.RESIDENTIAL_HOTELS_MULTIFAMILY_PRIVATE
        logger.info(
            f"Note: '{original_use}' is not a verbatim IBC Table 1607.1 category. "
            f"Rerouting to '{use}' (Private rooms and corridors serving them)."
        )

    requirements = get_minimum_live_load(use)
    min_uniform = requirements["uniform_psf"]
    min_concentrated = requirements["concentrated_lbs"]
    reduction_permitted = requirements["reduction_permitted"]

    # 2. Handle Public Restrooms Specific Logic
    if use == LiveLoadUse.PUBLIC_RESTROOMS:
        logger.info(
            "Note: Public restroom live loads are 'Same as area served' "
            "but not required to exceed 60 psf. Currently validating against 60 psf."
        )

    # 3. Inform about Live Load Reduction
    if not reduction_permitted:
        logger.info(f"Note: Live load reduction is not permitted for {use}.")

    # 4. Handle No-op / Section Reference cases
    if min_uniform is None and min_concentrated is None:
        return ComplianceResult(
            status=ComplianceStatus.NOT_APPLICABLE,
            message=(
                f"[NOT_APPLICABLE] Live load requirements for {use} "
                "reference other code sections and are not currently "
                "validated by this specific function."
            ),
        )

    # 2. Validate Uniform Load
    if min_uniform is not None and design_uniform_psf < min_uniform:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f"[FAIL] Uniform live load {design_uniform_psf} psf is below "
                f"the {min_uniform} psf minimum required for {use}."
            ),
        )

    # 3. Validate Concentrated Load (if required)
    if min_concentrated is not None:
        if design_concentrated_lbs is None:
            return ComplianceResult(
                status=ComplianceStatus.FAIL,
                message=(
                    f"[FAIL] Concentrated live load is required for {use} "
                    f"({min_concentrated} lbs minimum), but none was provided."
                ),
            )
        if design_concentrated_lbs < min_concentrated:
            return ComplianceResult(
                status=ComplianceStatus.FAIL,
                message=(
                    f"[FAIL] Concentrated live load {design_concentrated_lbs} lbs "
                    f"is below the {min_concentrated} lbs minimum required for {use}."
                ),
            )

    return ComplianceResult(status=ComplianceStatus.PASS)
