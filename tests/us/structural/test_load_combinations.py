import pytest

from aeclib.us.structural.load_combinations import DesignMethod, get_load_combinations


def test_get_load_combinations_only_dead():
    dead = {"P": 100.0, "Mx": 10.0}

    # Test LRFD only
    results_lrfd = get_load_combinations(dead=dead, method=DesignMethod.LRFD)
    assert len(results_lrfd) > 0
    assert "LRFD_1" in results_lrfd
    assert "ASD_1" not in results_lrfd

    case_lrfd_1 = results_lrfd["LRFD_1"]
    assert case_lrfd_1["formula"] == "1.4D"
    assert case_lrfd_1["method"] == "LRFD"
    assert case_lrfd_1["values"]["P"] == 140.0
    assert case_lrfd_1["values"]["Mx"] == 14.0

    # Test ASD only
    results_asd = get_load_combinations(dead=dead, method=DesignMethod.ASD)
    assert len(results_asd) > 0
    assert "ASD_1" in results_asd
    assert "LRFD_1" not in results_asd

    case_asd_1 = results_asd["ASD_1"]
    assert case_asd_1["formula"] == "D"
    assert case_asd_1["method"] == "ASD"
    assert case_asd_1["values"]["P"] == 100.0
    assert case_asd_1["values"]["Mx"] == 10.0


def test_get_load_combinations_dead_and_live():
    dead = {"P": 100.0, "Mx": 10.0}
    live = {"P": 50.0, "My": 20.0}

    results = get_load_combinations(dead=dead, live=live, method=DesignMethod.BOTH)

    # Check key union resolution: both P, Mx, and My should exist in results
    case_lrfd_2 = results["LRFD_2_Lr"]
    assert case_lrfd_2["values"]["P"] == 1.2 * 100.0 + 1.6 * 50.0  # 120 + 80 = 200
    assert case_lrfd_2["values"]["Mx"] == 1.2 * 10.0 + 1.6 * 0.0  # 12
    assert case_lrfd_2["values"]["My"] == 1.2 * 0.0 + 1.6 * 20.0  # 32

    case_asd_2 = results["ASD_2"]
    assert case_asd_2["values"]["P"] == 150.0
    assert case_asd_2["values"]["Mx"] == 10.0
    assert case_asd_2["values"]["My"] == 20.0


def test_get_load_combinations_directionality():
    dead = {"P": 100.0}
    wind = {"Mx": 50.0}

    # Wind expands into pos and neg cases natively
    results = get_load_combinations(dead=dead, wind=wind, method=DesignMethod.LRFD)
    assert "LRFD_6_pos" in results
    assert "LRFD_6_neg" in results

    assert results["LRFD_6_pos"]["values"]["Mx"] == 50.0
    assert results["LRFD_6_neg"]["values"]["Mx"] == -50.0


def test_get_load_combinations_all_components():
    dead = {"P": 100.0}
    live = {"P": 50.0}
    roof_live = {"P": 20.0}
    snow = {"P": 30.0}
    rain = {"P": 10.0}
    wind = {"P": 40.0}
    seismic = {"P": 25.0}

    results = get_load_combinations(
        dead=dead,
        live=live,
        roof_live=roof_live,
        snow=snow,
        rain=rain,
        wind=wind,
        seismic=seismic,
        method=DesignMethod.BOTH,
    )

    # Validate LRFD Case 4 with Roof Live
    # Formula: 1.2D + 1.0W + 1.0L + 0.5Lr
    # Values: 1.2*100 + 1.0*40 + 1.0*50 + 0.5*20 = 120 + 40 + 50 + 10 = 220
    assert results["LRFD_4_Lr_pos"]["values"]["P"] == 220.0

    # Validate LRFD Case 4 with Roof Live (neg Wind)
    # Formula: 1.2D - 1.0W + 1.0L + 0.5Lr
    # Values: 1.2*100 - 1.0*40 + 1.0*50 + 0.5*20 = 120 - 40 + 50 + 10 = 140
    assert results["LRFD_4_Lr_neg"]["values"]["P"] == 140.0


def test_get_load_combinations_errors_and_edge_cases():
    # Empty inputs
    assert get_load_combinations(dead={}) == {}

    # Invalid design method
    with pytest.raises(ValueError, match="Invalid design method specified"):
        get_load_combinations(dead={"P": 10.0}, method="invalid_method")
