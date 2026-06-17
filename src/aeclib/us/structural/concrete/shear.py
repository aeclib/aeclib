def calculate_one_way_shear_capacity(
    concrete_strength_psi: float,
    width_in: float,
    effective_depth_in: float,
) -> float:
    """
    Calculates the design one-way shear strength (phi * Vc) of a concrete member
    without shear reinforcement.

    Applicable to:
    - ACI 318-25 Section 22.5

    Args:
        concrete_strength_psi: Concrete compressive strength (f'c) in psi.
        width_in: Width of the critical section in inches (normally footing width b).
        effective_depth_in: Effective depth of the footing in inches (d).

    Returns:
        The design one-way shear capacity in kips.
    """
    # phi = 0.75 for shear (ACI 318-25 Table 21.2.1)
    phi = 0.75
    # Vc = 2 * lambda * sqrt(f'c) * b * d
    # Assuming lambda = 1.0 (normal weight concrete)
    lambda_factor = 1.0
    V_c = 2.0 * lambda_factor * (concrete_strength_psi**0.5) * width_in * effective_depth_in
    return (phi * V_c) / 1000.0


def calculate_two_way_shear_capacity(
    concrete_strength_psi: float,
    column_width_in: float,
    column_length_in: float,
    effective_depth_in: float,
    column_type: str = "interior",
) -> float:
    """
    Calculates the design two-way (punching) shear strength (phi * Vc) of a concrete
    footing at the critical section (d/2 from the column face).

    Applicable to:
    - ACI 318-25 Section 22.6.5.2

    Args:
        concrete_strength_psi: Concrete compressive strength (f'c) in psi.
        column_width_in: Column dimension in the width direction.
        column_length_in: Column dimension in the length direction.
        effective_depth_in: Effective depth of the footing in inches (d).
        column_type: Location category ("interior", "edge", or "corner").

    Returns:
        The design punching shear capacity in kips.
    """
    phi = 0.75
    lambda_factor = 1.0

    # 1. Critical perimeter b0 (rectangular perimeter at d/2 from column face)
    b0 = 2.0 * (column_width_in + effective_depth_in) + 2.0 * (column_length_in + effective_depth_in)

    # 2. Ratio of long to short column dimension (beta)
    col_max = max(column_width_in, column_length_in)
    col_min = min(column_width_in, column_length_in)
    beta = col_max / col_min if col_min > 0 else 1.0

    # 3. Column location constant alpha_s
    if column_type == "interior":
        alpha_s = 40.0
    elif column_type == "edge":
        alpha_s = 30.0
    else:
        alpha_s = 20.0

    # 4. Three ACI punching shear equations (limiting concrete nominal stress v_c)
    # Eq a: (2 + 4/beta) * lambda * sqrt(f'c)
    vc_a = (2.0 + 4.0 / beta) * lambda_factor * (concrete_strength_psi**0.5)

    # Eq b: (alpha_s * d / b0 + 2) * lambda * sqrt(f'c)
    vc_b = ((alpha_s * effective_depth_in / b0) + 2.0) * lambda_factor * (concrete_strength_psi**0.5)

    # Eq c: 4 * lambda * sqrt(f'c)
    vc_c = 4.0 * lambda_factor * (concrete_strength_psi**0.5)

    # Governing nominal shear stress (minimum of the three)
    vc_min = min(vc_a, vc_b, vc_c)

    # Nominal punching shear force V_c = v_c * b0 * d
    V_c = vc_min * b0 * effective_depth_in

    return (phi * V_c) / 1000.0
