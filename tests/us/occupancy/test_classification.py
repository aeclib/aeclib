from aeclib.us.common.occupancy import (
    Occupancy,
    get_base_classification,
    is_base_classification,
)
from aeclib.us.occupancy.classification import (
    determine_assembly_classification,
    determine_care_classification,
    determine_residential_classification,
)


def test_base_classification_utilities():
    assert get_base_classification(Occupancy.GROUP_A_2) == Occupancy.GROUP_A
    assert get_base_classification(Occupancy.GROUP_B) == Occupancy.GROUP_B
    assert get_base_classification(Occupancy.GROUP_I_4) == Occupancy.GROUP_I

    assert is_base_classification(Occupancy.GROUP_H_3, Occupancy.GROUP_H) is True
    assert is_base_classification(Occupancy.GROUP_A_1, Occupancy.GROUP_B) is False


def test_determine_assembly_classification():
    # Small accessory assembly -> Group B
    assert determine_assembly_classification(occupant_load=49, area=800.0, is_accessory=True) == Occupancy.GROUP_B
    # Small area accessory assembly -> Group B
    assert determine_assembly_classification(occupant_load=100, area=700.0, is_accessory=True) == Occupancy.GROUP_B
    # Non-accessory -> Group A
    assert determine_assembly_classification(occupant_load=49, area=800.0, is_accessory=False) == Occupancy.GROUP_A
    # Large accessory -> Group A
    assert determine_assembly_classification(occupant_load=60, area=800.0, is_accessory=True) == Occupancy.GROUP_A


def test_determine_care_classification():
    # Under 2.5 yrs, > 5 kids -> I-4
    assert (
        determine_care_classification(occupant_count=6, age_under_2_5=True, is_24_hour_care=False)
        == Occupancy.GROUP_I_4
    )
    # Under 2.5 yrs, <= 5 kids -> R-3
    assert (
        determine_care_classification(occupant_count=5, age_under_2_5=True, is_24_hour_care=False)
        == Occupancy.GROUP_R_3
    )

    # 24 hour care, > 16 people -> I-1
    assert (
        determine_care_classification(occupant_count=20, age_under_2_5=False, is_24_hour_care=True)
        == Occupancy.GROUP_I_1
    )
    # 24 hour care, 6-16 people -> R-4
    assert (
        determine_care_classification(occupant_count=10, age_under_2_5=False, is_24_hour_care=True)
        == Occupancy.GROUP_R_4
    )
    # 24 hour care, <= 5 people -> R-3
    assert (
        determine_care_classification(occupant_count=5, age_under_2_5=False, is_24_hour_care=True)
        == Occupancy.GROUP_R_3
    )

    # Not under 2.5, not 24 hr -> E
    assert (
        determine_care_classification(occupant_count=50, age_under_2_5=False, is_24_hour_care=False)
        == Occupancy.GROUP_E
    )


def test_determine_residential_classification():
    # Transient <= 10 -> R-3
    assert determine_residential_classification(is_transient=True, occupant_count=10) == Occupancy.GROUP_R_3
    # Transient > 10 -> R-1
    assert determine_residential_classification(is_transient=True, occupant_count=11) == Occupancy.GROUP_R_1
    # Nontransient > 16 -> R-2
    assert determine_residential_classification(is_transient=False, occupant_count=17) == Occupancy.GROUP_R_2
    # Nontransient <= 16 -> R-3
    assert determine_residential_classification(is_transient=False, occupant_count=16) == Occupancy.GROUP_R_3
