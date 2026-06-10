def validate_mezzanine_area(
    mezzanine_area: float,
    room_area: float,
    is_type_i_or_ii: bool = False,
    is_fully_sprinklered: bool = False,
    has_voice_alarm: bool = False,
) -> bool:
    """
    Validates if a mezzanine area complies with the area limitations.

    Applicable to:
    - IBC 2024 Section 505.2.1

    The clear area of a mezzanine shall not exceed one-third of the clear area
    of the room in which it is located.
    Exception: The area can be up to one-half if the building is Type I or II,
    fully sprinklered, and has an emergency voice/alarm communication system.

    Args:
        mezzanine_area: The area of the mezzanine.
        room_area: The area of the room in which the mezzanine is located.
        is_type_i_or_ii: True if the building is Type I or Type II construction.
        is_fully_sprinklered: True if the building is equipped throughout with an automatic sprinkler system.
        has_voice_alarm: True if the building has an emergency voice/alarm communication system.

    Returns:
        True if the mezzanine area complies with the limitations, False otherwise.
    """
    if room_area <= 0:
        return False

    if is_type_i_or_ii and is_fully_sprinklered and has_voice_alarm:
        return mezzanine_area <= (room_area / 2.0)

    return mezzanine_area <= (room_area / 3.0)
