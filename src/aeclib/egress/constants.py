from enum import Enum


class AreaBasis(str, Enum):
    """Specifies whether a calculation is based on Gross or Net area."""

    GROSS = "gross"
    NET = "net"


class SpaceFunction(str, Enum):
    """
    Standardized functional categories for spaces.
    These keys are used to look up factors and area basis.
    """

    ACCESSORY_STORAGE = "accessory_storage"
    AGRICULTURAL = "agricultural"
    AIRCRAFT_HANGARS = "aircraft_hangars"
    AIRPORT_BAGGAGE_CLAIM = "airport_baggage_claim"
    AIRPORT_BAGGAGE_HANDLING = "airport_baggage_handling"
    AIRPORT_CONCOURSE = "airport_concourse"
    AIRPORT_WAITING_AREAS = "airport_waiting_areas"
    ASSEMBLY_GAMING = "assembly_gaming"
    ASSEMBLY_EXHIBIT = "assembly_exhibit"
    ASSEMBLY_CONCENTRATED = "assembly_concentrated"
    ASSEMBLY_STANDING = "assembly_standing"
    ASSEMBLY_UNCONCENTRATED = "assembly_unconcentrated"
    BUSINESS = "business"
    COURTROOM = "courtroom"
    DAY_CARE = "day_care"
    DORMITORY = "dormitory"
    EDUCATIONAL_CLASSROOM = "educational_classroom"
    EDUCATIONAL_SHOP = "educational_shop"
    EXERCISE_ROOM = "exercise_room"
    INDUSTRIAL = "industrial"
    INSTITUTIONAL_INPATIENT = "institutional_inpatient"
    INSTITUTIONAL_OUTPATIENT = "institutional_outpatient"
    INSTITUTIONAL_SLEEPING = "institutional_sleeping"
    KITCHEN_COMMERCIAL = "kitchen_commercial"
    LIBRARY_READING = "library_reading"
    LIBRARY_STACK = "library_stack"
    LOCKER_ROOM = "locker_room"
    MERCANTILE = "mercantile"
    MERCANTILE_STORAGE = "mercantile_storage"
    PARKING_GARAGE = "parking_garage"
    RESIDENTIAL = "residential"
    SWIMMING_POOL = "swimming_pool"
    SWIMMING_POOL_DECK = "swimming_pool_deck"
    STAGE_PLATFORM = "stage_platform"
    WAREHOUSE = "warehouse"


# This mapping represents the 'Legal Knowledge' of Table 1004.5.
# It pairs each function with its required Area Basis and Load Factor.
MAXIMUM_FLOOR_AREA_ALLOWANCES_PER_OCCUPANT = {
    SpaceFunction.ACCESSORY_STORAGE: {"factor": 300, "basis": AreaBasis.GROSS},
    SpaceFunction.AGRICULTURAL: {"factor": 300, "basis": AreaBasis.GROSS},
    SpaceFunction.AIRCRAFT_HANGARS: {"factor": 500, "basis": AreaBasis.GROSS},
    SpaceFunction.AIRPORT_BAGGAGE_CLAIM: {"factor": 20, "basis": AreaBasis.GROSS},
    SpaceFunction.AIRPORT_BAGGAGE_HANDLING: {"factor": 300, "basis": AreaBasis.GROSS},
    SpaceFunction.AIRPORT_CONCOURSE: {"factor": 100, "basis": AreaBasis.GROSS},
    SpaceFunction.AIRPORT_WAITING_AREAS: {"factor": 15, "basis": AreaBasis.GROSS},
    SpaceFunction.ASSEMBLY_GAMING: {"factor": 11, "basis": AreaBasis.GROSS},
    SpaceFunction.ASSEMBLY_EXHIBIT: {"factor": 30, "basis": AreaBasis.NET},
    SpaceFunction.ASSEMBLY_CONCENTRATED: {"factor": 7, "basis": AreaBasis.NET},
    SpaceFunction.ASSEMBLY_STANDING: {"factor": 5, "basis": AreaBasis.NET},
    SpaceFunction.ASSEMBLY_UNCONCENTRATED: {"factor": 15, "basis": AreaBasis.NET},
    SpaceFunction.BUSINESS: {"factor": 150, "basis": AreaBasis.GROSS},
    SpaceFunction.COURTROOM: {"factor": 40, "basis": AreaBasis.NET},
    SpaceFunction.DAY_CARE: {"factor": 35, "basis": AreaBasis.NET},
    SpaceFunction.DORMITORY: {"factor": 50, "basis": AreaBasis.GROSS},
    SpaceFunction.EDUCATIONAL_CLASSROOM: {"factor": 20, "basis": AreaBasis.NET},
    SpaceFunction.EDUCATIONAL_SHOP: {"factor": 50, "basis": AreaBasis.NET},
    SpaceFunction.EXERCISE_ROOM: {"factor": 50, "basis": AreaBasis.GROSS},
    SpaceFunction.INDUSTRIAL: {"factor": 100, "basis": AreaBasis.GROSS},
    SpaceFunction.INSTITUTIONAL_INPATIENT: {"factor": 240, "basis": AreaBasis.GROSS},
    SpaceFunction.INSTITUTIONAL_OUTPATIENT: {"factor": 100, "basis": AreaBasis.GROSS},
    SpaceFunction.INSTITUTIONAL_SLEEPING: {"factor": 120, "basis": AreaBasis.GROSS},
    SpaceFunction.KITCHEN_COMMERCIAL: {"factor": 200, "basis": AreaBasis.GROSS},
    SpaceFunction.LIBRARY_READING: {"factor": 50, "basis": AreaBasis.NET},
    SpaceFunction.LIBRARY_STACK: {"factor": 100, "basis": AreaBasis.GROSS},
    SpaceFunction.LOCKER_ROOM: {"factor": 50, "basis": AreaBasis.GROSS},
    SpaceFunction.MERCANTILE: {"factor": 60, "basis": AreaBasis.GROSS},
    SpaceFunction.MERCANTILE_STORAGE: {"factor": 300, "basis": AreaBasis.GROSS},
    SpaceFunction.PARKING_GARAGE: {"factor": 200, "basis": AreaBasis.GROSS},
    SpaceFunction.RESIDENTIAL: {"factor": 200, "basis": AreaBasis.GROSS},
    SpaceFunction.SWIMMING_POOL: {"factor": 50, "basis": AreaBasis.GROSS},
    SpaceFunction.SWIMMING_POOL_DECK: {"factor": 15, "basis": AreaBasis.GROSS},
    SpaceFunction.STAGE_PLATFORM: {"factor": 15, "basis": AreaBasis.NET},
    SpaceFunction.WAREHOUSE: {"factor": 500, "basis": AreaBasis.GROSS},
}
