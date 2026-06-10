from aeclib.us.building.mixed_use import (
    StoryOccupancyArea,
    calculate_allowable_area,
    calculate_sum_of_ratios,
    validate_accessory_occupancy,
    validate_nonseparated_occupancies,
    validate_separated_occupancies,
)
from aeclib.us.common.construction_type import ConstructionType
from aeclib.us.common.occupancy import Occupancy
from aeclib.us.common.sprinklers import SprinklerSystem


def test_validate_accessory_occupancy():
    # 10% exactly is allowed
    assert validate_accessory_occupancy(1000.0, 10000.0) is True

    # Less than 10% is allowed
    assert validate_accessory_occupancy(500.0, 10000.0) is True

    # More than 10% is not allowed
    assert validate_accessory_occupancy(1100.0, 10000.0) is False

    # Zero total area edge case
    assert validate_accessory_occupancy(100.0, 0.0) is False


def test_calculate_allowable_area():
    # Base area 10,000 + 25% frontage increase (0.25) = 12,500
    assert calculate_allowable_area(10000.0, 0.25) == 12500.0

    # Base area 10,000 + 0% frontage increase = 10,000
    assert calculate_allowable_area(10000.0, 0.0) == 10000.0


def test_calculate_sum_of_ratios():
    # Scenario: Group B and Group R-2
    # Type IIB, Non-Sprinklered, 1 story
    # For Group B, At = 23,000 sq ft.
    # For Group R-2, At = 16,000 sq ft.

    occupancies = [
        StoryOccupancyArea(Occupancy.GROUP_B, 11500.0),  # Ratio: 11,500 / 23,000 = 0.50
        StoryOccupancyArea(Occupancy.GROUP_R_2, 4000.0),  # Ratio:  4,000 / 16,000 = 0.25
    ]

    sum_ratios = calculate_sum_of_ratios(
        occupancy_areas=occupancies,
        construction_type=ConstructionType.TYPE_II_B,
        sprinkler_system=SprinklerSystem.NOT_SPRINKLERED,
        stories=1,
        frontage_increase=0.0,
    )

    # 0.50 + 0.25 = 0.75
    assert sum_ratios == 0.75


def test_calculate_sum_of_ratios_with_frontage():
    # Scenario: Group B and Group R-2
    # Type IIB, Non-Sprinklered, 1 story
    # For Group B, At = 23,000 sq ft.
    # For Group R-2, At = 16,000 sq ft.
    # If = 0.25 (25% frontage increase)
    # Aa (Group B) = 23,000 * 1.25 = 28,750
    # Aa (Group R-2) = 16,000 * 1.25 = 20,000

    occupancies = [
        StoryOccupancyArea(Occupancy.GROUP_B, 14375.0),  # Ratio: 14,375 / 28,750 = 0.50
        StoryOccupancyArea(Occupancy.GROUP_R_2, 5000.0),  # Ratio:  5,000 / 20,000 = 0.25
    ]

    sum_ratios = calculate_sum_of_ratios(
        occupancy_areas=occupancies,
        construction_type=ConstructionType.TYPE_II_B,
        sprinkler_system=SprinklerSystem.NOT_SPRINKLERED,
        stories=1,
        frontage_increase=0.25,
    )

    # 0.50 + 0.25 = 0.75
    assert sum_ratios == 0.75


def test_calculate_sum_of_ratios_unlimited():
    # Scenario: Group B in Type IA is "UL" (Unlimited)
    occupancies = [
        StoryOccupancyArea(Occupancy.GROUP_B, 1000000.0),
    ]

    sum_ratios = calculate_sum_of_ratios(
        occupancy_areas=occupancies,
        construction_type=ConstructionType.TYPE_I_A,
        sprinkler_system=SprinklerSystem.NOT_SPRINKLERED,
        stories=1,
        frontage_increase=0.0,
    )

    # Unlimited area -> ratio of 0
    assert sum_ratios == 0.0


def test_validate_nonseparated_occupancies():
    # Group B At = 23,000. Group R-2 At = 16,000.
    # Most restrictive is 16,000.

    # Total area 15,000 -> Valid
    occupancies_valid = [
        StoryOccupancyArea(Occupancy.GROUP_B, 10000.0),
        StoryOccupancyArea(Occupancy.GROUP_R_2, 5000.0),
    ]
    assert (
        validate_nonseparated_occupancies(
            occupancies_valid, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED, 1
        )
        is True
    )

    # Total area 17,000 -> Invalid
    occupancies_invalid = [
        StoryOccupancyArea(Occupancy.GROUP_B, 12000.0),
        StoryOccupancyArea(Occupancy.GROUP_R_2, 5000.0),
    ]
    assert (
        validate_nonseparated_occupancies(
            occupancies_invalid, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED, 1
        )
        is False
    )


def test_validate_separated_occupancies():
    # Ratio sum 0.75 -> Valid
    occupancies_valid = [
        StoryOccupancyArea(Occupancy.GROUP_B, 11500.0),  # 0.50
        StoryOccupancyArea(Occupancy.GROUP_R_2, 4000.0),  # 0.25
    ]
    assert (
        validate_separated_occupancies(
            occupancies_valid, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED, 1
        )
        is True
    )

    # Ratio sum 1.25 -> Invalid
    occupancies_invalid = [
        StoryOccupancyArea(Occupancy.GROUP_B, 23000.0),  # 1.00
        StoryOccupancyArea(Occupancy.GROUP_R_2, 4000.0),  # 0.25
    ]
    assert (
        validate_separated_occupancies(
            occupancies_invalid, ConstructionType.TYPE_II_B, SprinklerSystem.NOT_SPRINKLERED, 1
        )
        is False
    )
