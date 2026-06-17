from dataclasses import dataclass

from aeclib.core import ComplianceResult, ComplianceStatus


@dataclass
class RebarProperties:
    nominal_diameter_in: float
    area_sq_in: float
    weight_lb_ft: float


# Standard US deformed bar properties mapping bar size to properties
REBAR_PROPERTIES = {
    3: RebarProperties(0.375, 0.11, 0.376),
    4: RebarProperties(0.500, 0.20, 0.668),
    5: RebarProperties(0.625, 0.31, 1.043),
    6: RebarProperties(0.750, 0.44, 1.502),
    7: RebarProperties(0.875, 0.60, 2.044),
    8: RebarProperties(1.000, 0.79, 2.670),
    9: RebarProperties(1.128, 1.00, 3.400),
    10: RebarProperties(1.270, 1.27, 4.303),
    11: RebarProperties(1.410, 1.56, 5.313),
    14: RebarProperties(1.693, 2.25, 7.650),
    18: RebarProperties(2.257, 4.00, 13.600),
}


def validate_minimum_reinforcement(
    steel_area_sq_in: float,
    width_in: float,
    thickness_in: float,
) -> ComplianceResult:
    """
    Validates reinforcement steel area against ACI 318 minimum temperature
    and shrinkage reinforcement limits (As_min = 0.0018 * b * h).

    Applicable to:
    - ACI 318-25 Section 24.4.3.2

    Args:
        steel_area_sq_in: Proposed reinforcement area in square inches.
        width_in: Footing width in inches (b).
        thickness_in: Footing thickness/height in inches (h).

    Returns:
        ComplianceResult (PASS or FAIL).
    """
    min_ratio = 0.0018
    as_min = min_ratio * width_in * thickness_in

    if steel_area_sq_in < as_min:
        return ComplianceResult(
            status=ComplianceStatus.FAIL,
            message=(
                f"[FAIL] Steel area {steel_area_sq_in:.3f} sq in is less than the ACI 318 "
                f"minimum temperature/shrinkage steel area of {as_min:.3f} sq in (0.0018 * b * h)."
            ),
        )

    return ComplianceResult(status=ComplianceStatus.PASS)


def calculate_development_length(
    bar_size: int,
    steel_yield_strength_psi: float,
    concrete_strength_psi: float,
    is_top_bar: bool = False,
    is_epoxy_coated: bool = False,
) -> float:
    """
    Calculates the tension development length (l_d) in inches for deformed bars
    according to ACI 318 simplified equations.

    Applicable to:
    - ACI 318-25 Section 25.4.2

    Args:
        bar_size: Standard US bar size number (3 through 11).
        steel_yield_strength_psi: Reinforcement yield strength (fy) in psi.
        concrete_strength_psi: Concrete compressive strength (f'c) in psi.
        is_top_bar: True if the bar is a horizontal top bar cast with > 12 in concrete below.
        is_epoxy_coated: True if the reinforcement is epoxy coated.

    Returns:
        The calculated tension development length in inches (minimum 12.0 inches).
    """
    if bar_size not in REBAR_PROPERTIES:
        raise ValueError(f"Unsupported bar size: #{bar_size}. Supported sizes: {list(REBAR_PROPERTIES.keys())}")

    d_b = REBAR_PROPERTIES[bar_size].nominal_diameter_in

    # Modification factors
    psi_t = 1.3 if is_top_bar else 1.0
    psi_e = 1.2 if is_epoxy_coated else 1.0

    # Product of psi_t * psi_e need not exceed 1.7 (ACI 25.4.2.4)
    if psi_t * psi_e > 1.7:
        psi_product = 1.7
    else:
        psi_product = psi_t * psi_e

    psi_g = 1.0  # Grade 60 (fy = 60,000 psi)
    lambda_factor = 1.0  # Normal weight concrete

    # Choose equation based on bar size
    if bar_size <= 6:
        numerator = steel_yield_strength_psi * psi_product * psi_g
        denominator = 25.0 * lambda_factor * (concrete_strength_psi**0.5)
    else:
        numerator = steel_yield_strength_psi * psi_product * psi_g
        denominator = 20.0 * lambda_factor * (concrete_strength_psi**0.5)

    l_d = (numerator / denominator) * d_b

    # Absolute minimum tension development length is 12 inches (ACI 25.4.2.1)
    return max(12.0, l_d)


def calculate_hooked_development_length(
    bar_size: int,
    steel_yield_strength_psi: float,
    concrete_strength_psi: float,
    is_epoxy_coated: bool = False,
) -> float:
    """
    Calculates the tension development length (l_dh) in inches for a standard hook
    according to ACI 318 simplified equations.

    Applicable to:
    - ACI 318-25 Section 25.4.3

    Args:
        bar_size: Standard US bar size number (3 through 11).
        steel_yield_strength_psi: Reinforcement yield strength (fy) in psi.
        concrete_strength_psi: Concrete compressive strength (f'c) in psi.
        is_epoxy_coated: True if the reinforcement is epoxy coated.

    Returns:
        The calculated tension development length for a hook in inches.
    """
    if bar_size not in REBAR_PROPERTIES:
        raise ValueError(f"Unsupported bar size: #{bar_size}. Supported sizes: {list(REBAR_PROPERTIES.keys())}")

    d_b = REBAR_PROPERTIES[bar_size].nominal_diameter_in

    psi_e = 1.2 if is_epoxy_coated else 1.0
    lambda_factor = 1.0  # Normal weight concrete

    # Basic development length for standard hook
    l_dh = (0.02 * psi_e * steel_yield_strength_psi / (lambda_factor * (concrete_strength_psi**0.5))) * d_b

    # Absolute minimums: 8 * d_b or 6 inches
    return max(l_dh, 8.0 * d_b, 6.0)
