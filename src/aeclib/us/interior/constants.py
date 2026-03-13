from enum import Enum

from aeclib.us.common.dimensions import (
    MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
    MINIMUM_CEILING_HEIGHT_STANDARD_INCHES,
)


class RoomType(str, Enum):
    """
    Categorization of rooms based on their primary function
    for environmental standards.
    """

    # Standard (7' 6")
    HABITABLE = "habitable"
    OCCUPIABLE = "occupiable"
    CORRIDOR = "corridor"

    # Service (7' 0")
    BATHROOM = "bathroom"
    TOILET_ROOM = "toilet_room"
    KITCHEN = "kitchen"
    STORAGE_ROOM = "storage_room"
    LAUNDRY_ROOM = "laundry_room"


# Mapping of RoomTypes to their standard minimum height thresholds.
ROOM_HEIGHT_THRESHOLDS = {
    RoomType.HABITABLE: MINIMUM_CEILING_HEIGHT_STANDARD_INCHES,
    RoomType.OCCUPIABLE: MINIMUM_CEILING_HEIGHT_STANDARD_INCHES,
    RoomType.CORRIDOR: MINIMUM_CEILING_HEIGHT_STANDARD_INCHES,
    RoomType.BATHROOM: MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
    RoomType.TOILET_ROOM: MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
    RoomType.KITCHEN: MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
    RoomType.STORAGE_ROOM: MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
    RoomType.LAUNDRY_ROOM: MINIMUM_CEILING_HEIGHT_SERVICE_INCHES,
}
