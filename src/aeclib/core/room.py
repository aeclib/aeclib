from enum import Enum


class RoomType(str, Enum):
    """
    Standardized functional categories for rooms used across disciplines.
    """

    # Standard Functional Rooms
    BATHROOM = "bathroom"
    KITCHEN = "kitchen"
    STORAGE_ROOM = "storage_room"
    LAUNDRY_ROOM = "laundry_room"
    CORRIDOR = "corridor"

    # Mezzanines
    MEZZANINE = "mezzanine"
    BELOW_MEZZANINE = "below_mezzanine"

    # Parking (Public or Private Structures, NOT residential garages)
    PARKING_GARAGE = "parking_garage"

    # Non-Occupiable / Non-Habitable
    ATTIC = "attic"
    CRAWL_SPACE = "crawl_space"
    MECHANICAL_ROOM = "mechanical_room"
