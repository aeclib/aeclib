import logging
from typing import Optional, Union

from . import constants
from .constants import DesignMethod

logger = logging.getLogger("aeclib")


def get_load_combinations(
    dead: dict[str, float],
    live: Optional[dict[str, float]] = None,
    roof_live: Optional[dict[str, float]] = None,
    snow: Optional[dict[str, float]] = None,
    rain: Optional[dict[str, float]] = None,
    wind: Optional[dict[str, float]] = None,
    seismic: Optional[dict[str, float]] = None,
    method: Union[DesignMethod, str] = DesignMethod.BOTH,
) -> dict[str, dict]:
    """
    Computes ASCE 7-16 / IBC load combinations for given component loads.

    Applicable to:
    - ASCE 7-16 Chapter 2
    - IBC 2024 Section 1605

    Args:
        dead: Dead load components (e.g., {"P": 10.0, "Mx": 5.0}).
        live: Live load components.
        roof_live: Roof live load components.
        snow: Snow load components.
        rain: Rain load components.
        wind: Wind load components.
        seismic: Seismic load components.
        method: The design method to use ("ASD", "LRFD", or "both").

    Returns:
        A dictionary mapping combination IDs to dictionaries containing:
        - "formula": The combination's mathematical formula.
        - "method": The design method used ("LRFD" or "ASD").
        - "values": Dict of combined load components (forces/moments).
    """
    # 1. Normalize inputs and collect all unique force/moment keys
    input_loads = {
        "dead": dead or {},
        "live": live or {},
        "roof_live": roof_live or {},
        "snow": snow or {},
        "rain": rain or {},
        "wind": wind or {},
        "seismic": seismic or {},
    }

    all_keys = set()
    for load_dict in input_loads.values():
        all_keys.update(load_dict.keys())

    if not all_keys:
        logger.info("No load components (forces/moments) provided in any load category.")
        return {}

    # Normalize method parameter
    if isinstance(method, DesignMethod):
        method_str = method.value.lower()
    else:
        method_str = str(method).lower()

    if method_str not in ("asd", "lrfd", "both"):
        raise ValueError(f"Invalid design method specified: {method}. Must be 'ASD', 'LRFD', or 'both'.")

    lrfd_list = [(t[0], t[1], t[2], DesignMethod.LRFD) for t in constants.LRFD_TEMPLATES]
    asd_list = [(t[0], t[1], t[2], DesignMethod.ASD) for t in constants.ASD_TEMPLATES]

    templates = []
    if method_str in ("lrfd", "both"):
        templates.extend(lrfd_list)
    if method_str in ("asd", "both"):
        templates.extend(asd_list)

    results = {}

    for case_id, formula, factors, design_method in templates:
        # Compute combined values for all keys
        combined_values = {}
        for key in all_keys:
            val = 0.0
            for comp_name, factor in factors.items():
                comp_val = input_loads[comp_name].get(key, 0.0)
                val += factor * comp_val
            combined_values[key] = val

        results[case_id] = {
            "formula": formula,
            "method": design_method.value.upper(),
            "values": combined_values,
        }

    return results
