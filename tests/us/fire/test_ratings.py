import pytest

from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.elements import BuildingElementCategory
from aeclib.us.fire.ratings import get_required_fire_resistance_rating


def test_primary_structural_frame_ratings():
    # Type IA needs 3 hours
    assert (
        get_required_fire_resistance_rating(ConstructionType.TYPE_I_A, BuildingElementCategory.PRIMARY_STRUCTURAL_FRAME)
        == 3.0
    )

    # Type IIB needs 0 hours
    assert (
        get_required_fire_resistance_rating(
            ConstructionType.TYPE_II_B, BuildingElementCategory.PRIMARY_STRUCTURAL_FRAME
        )
        == 0.0
    )

    # Type IV-HT uses Heavy Timber
    assert (
        get_required_fire_resistance_rating(
            ConstructionType.TYPE_IV_HT, BuildingElementCategory.PRIMARY_STRUCTURAL_FRAME
        )
        == "HT"
    )


def test_roof_support_reduction():
    # Type IA primary frame is 3 hours, but reduced to 2 if supporting roof only
    assert (
        get_required_fire_resistance_rating(
            ConstructionType.TYPE_I_A, BuildingElementCategory.PRIMARY_STRUCTURAL_FRAME, is_supporting_roof_only=True
        )
        == 2.0
    )

    # Type IIA bearing wall is 1 hour, reduced to 0 if supporting roof only
    assert (
        get_required_fire_resistance_rating(
            ConstructionType.TYPE_II_A, BuildingElementCategory.BEARING_WALL_EXTERIOR, is_supporting_roof_only=True
        )
        == 0.0
    )

    # Should not reduce floor construction even if supporting roof only flag is passed (doesn't apply)
    assert (
        get_required_fire_resistance_rating(
            ConstructionType.TYPE_I_A, BuildingElementCategory.FLOOR_CONSTRUCTION, is_supporting_roof_only=True
        )
        == 2.0
    )


def test_nonbearing_exterior_wall_raises_error():
    # Nonbearing exterior walls use Table 705.5
    with pytest.raises(ValueError):
        get_required_fire_resistance_rating(ConstructionType.TYPE_I_A, BuildingElementCategory.NONBEARING_WALL_EXTERIOR)


def test_unsupported_category_raises_error():
    with pytest.raises(ValueError):
        get_required_fire_resistance_rating(ConstructionType.TYPE_I_A, BuildingElementCategory.THERMAL_INSULATION)
