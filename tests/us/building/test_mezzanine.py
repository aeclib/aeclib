from aeclib.us.building.mezzanine import validate_mezzanine_area


def test_validate_mezzanine_area_standard():
    # 1/3 rule: 333 is <= 1000/3
    assert validate_mezzanine_area(333.0, 1000.0) is True
    # 1/3 rule: 334 is > 1000/3
    assert validate_mezzanine_area(334.0, 1000.0) is False


def test_validate_mezzanine_area_exception():
    # 1/2 rule exception met
    assert (
        validate_mezzanine_area(500.0, 1000.0, is_type_i_or_ii=True, is_fully_sprinklered=True, has_voice_alarm=True)
        is True
    )

    # 1/2 rule exception NOT met (missing voice alarm)
    assert (
        validate_mezzanine_area(500.0, 1000.0, is_type_i_or_ii=True, is_fully_sprinklered=True, has_voice_alarm=False)
        is False
    )


def test_validate_mezzanine_area_zero_room():
    # Edge case: zero or negative room area
    assert validate_mezzanine_area(100.0, 0.0) is False
    assert validate_mezzanine_area(100.0, -500.0) is False
