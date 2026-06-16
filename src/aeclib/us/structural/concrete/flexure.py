def calculate_required_flexural_steel_area(
    factored_moment_kip_ft: float,
    concrete_strength_psi: float,
    steel_yield_strength_psi: float,
    width_in: float,
    effective_depth_in: float,
) -> float:
    """
    Computes the required area of reinforcing steel (As) in square inches for a given
    factored bending moment (Mu) based on ACI 318 flexural design.

    Applicable to:
    - ACI 318-25 Section 22.2

    Args:
        factored_moment_kip_ft: Factored moment (Mu) in kip-feet.
        concrete_strength_psi: Concrete compressive strength (f'c) in psi.
        steel_yield_strength_psi: Reinforcement yield strength (fy) in psi.
        width_in: Footing width (or strip width) in inches (b).
        effective_depth_in: Effective depth of reinforcement in inches (d).

    Returns:
        The required reinforcement steel area in square inches.
    """
    if factored_moment_kip_ft <= 0.0:
        return 0.0

    # Convert Mu to lb-in
    M_u_lb_in = factored_moment_kip_ft * 12.0 * 1000.0

    # phi = 0.90 for flexure (tension-controlled section)
    phi = 0.90

    # R_n = Mu / (phi * b * d^2)
    R_n = M_u_lb_in / (phi * width_in * (effective_depth_in**2))

    # Check if section can handle moment in simple tension-controlled manner
    # rho = (0.85 * f'c / fy) * (1 - sqrt(1 - 2*Rn / (0.85 * f'c)))
    temp = 1.0 - (2.0 * R_n) / (0.85 * concrete_strength_psi)
    if temp < 0.0:
        # Re-check or section is too small; return max possible or let caller handle failure
        temp = 0.0

    rho = (0.85 * concrete_strength_psi / steel_yield_strength_psi) * (1.0 - (temp**0.5))
    return rho * width_in * effective_depth_in
