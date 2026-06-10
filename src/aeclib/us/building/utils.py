from typing import Dict, Union

from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem


def lookup_by_building_props(
    table: Dict,
    occupancy: Occupancy,
    category: Union[SprinklerSystem, str],
    construction_type: ConstructionType,
    data_type_name: str = "data",
) -> Union[float, int, str]:
    """
    Standardized lookup for IBC tabular data organized by [Occupancy][Category][ConstructionType].

    Category is typically a SprinklerSystem enum (for heights/stories) or
     a string like "NS", "S1", "SM" (for area).
    """
    if occupancy not in table:
        raise NotImplementedError(f"{data_type_name.capitalize()} for occupancy {occupancy} is not yet encoded.")

    category_data = table[occupancy]

    if category not in category_data:
        raise ValueError(f"Category {category} is not supported for occupancy {occupancy}.")

    return category_data[category][construction_type]
