import math

import pytest

from aeclib.core import ComplianceStatus
from aeclib.us.structural.concrete import (
    calculate_development_length,
    calculate_one_way_shear_capacity,
    calculate_required_flexural_steel_area,
    calculate_two_way_shear_capacity,
    validate_minimum_reinforcement,
)


def test_calculate_one_way_shear_capacity():
    # Example: f'c = 3000 psi, b = 12 in, d = 10 in
    # Vc = 2 * sqrt(3000) * 12 * 10 = 13145.34 lb
    # phi*Vc = 0.75 * 13145.34 / 1000 = 9.859 kips
    phi_vc = calculate_one_way_shear_capacity(
        concrete_strength_psi=3000.0,
        width_in=12.0,
        effective_depth_in=10.0,
    )
    assert math.isclose(phi_vc, 9.859, rel_tol=0.01)


def test_calculate_two_way_shear_capacity():
    # Example: f'c = 3000 psi, interior column 12x12, d = 10
    # b0 = 2*(12+10) + 2*(12+10) = 88 in
    # v_c limit will be Eq (c): 4 * sqrt(3000) = 219.089 psi
    # Vc = 219.089 * 88 * 10 = 192798 lb
    # phi*Vc = 0.75 * 192798 / 1000 = 144.598 kips
    phi_vc = calculate_two_way_shear_capacity(
        concrete_strength_psi=3000.0,
        column_width_in=12.0,
        column_length_in=12.0,
        effective_depth_in=10.0,
        column_type="interior",
    )
    assert math.isclose(phi_vc, 144.599, rel_tol=0.01)

    # Example: Edge column
    # alpha_s = 30. Eq (b) might govern if b0 is large.
    phi_vc_edge = calculate_two_way_shear_capacity(
        concrete_strength_psi=3000.0,
        column_width_in=12.0,
        column_length_in=12.0,
        effective_depth_in=10.0,
        column_type="edge",
    )
    # The equation still safely computes a capacity.
    assert phi_vc_edge > 0.0


def test_calculate_required_flexural_steel_area():
    # Example: Mu = 100 kip-ft, f'c = 3000, fy = 60000, b = 12, d = 10
    # Returns approximately 3.27 sq in
    ast = calculate_required_flexural_steel_area(
        factored_moment_kip_ft=100.0,
        concrete_strength_psi=3000.0,
        steel_yield_strength_psi=60000.0,
        width_in=12.0,
        effective_depth_in=10.0,
    )
    assert math.isclose(ast, 3.27, rel_tol=0.05)

    # Zero or negative moment should require zero flexural steel
    assert calculate_required_flexural_steel_area(-10.0, 3000, 60000, 12, 10) == 0.0

    # Very massive moment beyond section capacity
    # Causes math domain error internally (sqrt of negative) or handled gracefully
    ast_huge = calculate_required_flexural_steel_area(
        factored_moment_kip_ft=10000.0,
        concrete_strength_psi=3000.0,
        steel_yield_strength_psi=60000.0,
        width_in=12.0,
        effective_depth_in=10.0,
    )
    # Based on function logic, if Rn is too large, it sets temp = 0.0 and returns max valid rho
    # rho_max = 0.85 * f'c / fy * (1 - 0) = 0.0425 -> As = 0.0425 * 12 * 10 = 5.1
    assert math.isclose(ast_huge, 5.1, rel_tol=0.01)


def test_validate_minimum_reinforcement():
    # Minimum ratio 0.0018 * 12 * 12 = 0.2592
    res_pass = validate_minimum_reinforcement(0.3, width_in=12.0, thickness_in=12.0)
    assert res_pass.status == ComplianceStatus.PASS
    assert bool(res_pass) is True

    res_fail = validate_minimum_reinforcement(0.2, width_in=12.0, thickness_in=12.0)
    assert res_fail.status == ComplianceStatus.FAIL
    assert bool(res_fail) is False
    assert "less than" in res_fail.message


def test_calculate_development_length():
    # #5 bar, fy=60ksi, f'c=3ksi. Eq <= 6
    # ld = (60000 / (25 * sqrt(3000))) * 0.625 = 27.38 inches
    ld_5 = calculate_development_length(
        bar_size=5,
        steel_yield_strength_psi=60000.0,
        concrete_strength_psi=3000.0,
    )
    assert math.isclose(ld_5, 27.38, rel_tol=0.01)

    # #8 bar, fy=60ksi, f'c=3ksi. Eq > 6
    # ld = (60000 / (20 * sqrt(3000))) * 1.0 = 54.77 inches
    ld_8 = calculate_development_length(
        bar_size=8,
        steel_yield_strength_psi=60000.0,
        concrete_strength_psi=3000.0,
    )
    assert math.isclose(ld_8, 54.77, rel_tol=0.01)

    # Check top bar multiplier
    ld_5_top = calculate_development_length(
        bar_size=5,
        steel_yield_strength_psi=60000.0,
        concrete_strength_psi=3000.0,
        is_top_bar=True,
    )
    assert math.isclose(ld_5_top, 27.38 * 1.3, rel_tol=0.01)

    # Check max modifier limit (1.7)
    ld_5_max = calculate_development_length(
        bar_size=5,
        steel_yield_strength_psi=60000.0,
        concrete_strength_psi=3000.0,
        is_top_bar=True,  # 1.3
        is_epoxy_coated=True,  # 1.2
    )
    # 1.3 * 1.2 = 1.56, which is <= 1.7, so 1.56 is used.
    assert math.isclose(ld_5_max, 27.38 * 1.56, rel_tol=0.01)

    # Unsupported bar
    with pytest.raises(ValueError, match="Unsupported bar size"):
        calculate_development_length(2, 60000, 3000)
