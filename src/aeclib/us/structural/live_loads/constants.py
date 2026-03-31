from enum import Enum


class LiveLoadUse(str, Enum):
    """
    Standardized functional categories for live load requirements.
    Based on IBC 2024 Table 1607.1.
    """

    ACCESS_FLOOR_COMPUTER = "access_floor_computer"
    ACCESS_FLOOR_OFFICE = "access_floor_office"
    APARTMENTS = "apartments"
    ARMORIES_DRILL_ROOMS = "armories_drill_rooms"
    ASSEMBLY_FIXED_SEATS = "assembly_fixed_seats"
    ASSEMBLY_LOBBIES = "assembly_lobbies"
    ASSEMBLY_MOVABLE_SEATS = "assembly_movable_seats"
    ASSEMBLY_OTHER = "assembly_other"
    ASSEMBLY_STAGES_PLATFORMS = "assembly_stages_platforms"
    BALCONIES_DECKS = "balconies_decks"
    BOWLING_ALLEYS = "bowling_alleys"
    CATWALKS = "catwalks"
    CORRIDORS_FIRST_FLOOR = "corridors_first_floor"
    CORRIDORS_OTHER_FLOORS = "corridors_other_floors"
    DANCE_HALLS_BALLROOMS = "dance_halls_ballrooms"
    DINING_ROOMS_RESTAURANTS = "dining_rooms_restaurants"
    ELEVATOR_MACHINE_ROOM = "elevator_machine_room"
    FINISH_LIGHT_FLOOR_PLATE = "finish_light_floor_plate"
    FIRE_ESCAPES = "fire_escapes"
    FIXED_LADDER = "fixed_ladder"
    GARAGES_PASSENGER_VEHICLES = "garages_passenger_vehicles"
    GARAGES_TRUCKS_BUSES = "garages_trucks_buses"
    GRANDSTANDS = "grandstands"
    GYMNASIUMS = "gymnasiums"
    HANDRAILS_GUARDS = "handrails_guards"
    HELIPADS = "helipads"
    HOSPITALS_CORRIDORS_ABOVE_FIRST = "hospitals_corridors_above_first"
    HOSPITALS_OPERATING_LABS = "hospitals_operating_labs"
    HOSPITALS_PATIENT_ROOMS = "hospitals_patient_rooms"
    HOTELS = "hotels"
    LIBRARIES_CORRIDORS_ABOVE_FIRST = "libraries_corridors_above_first"
    LIBRARIES_READING_ROOMS = "libraries_reading_rooms"
    LIBRARIES_STACK_ROOMS = "libraries_stack_rooms"
    MANUFACTURING_HEAVY = "manufacturing_heavy"
    MANUFACTURING_LIGHT = "manufacturing_light"
    MARQUEES = "marquees"
    OFFICE_CORRIDORS_ABOVE_FIRST = "office_corridors_above_first"
    OFFICE_LOBBIES_FIRST_FLOOR_CORRIDORS = "office_lobbies_first_floor_corridors"
    OFFICE_OFFICES = "office_offices"
    PENAL_CELLS = "penal_cells"
    PENAL_CORRIDORS = "penal_corridors"
    PLATFORMS_ASSEMBLY = "platforms_assembly"
    PUBLIC_AREAS = "public_areas"
    PUBLIC_RESTROOMS = "public_restrooms"
    RECREATIONAL_AREAS = "recreational_areas"
    RESIDENTIAL_HABITABLE_ATTICS_SLEEPING = "residential_habitable_attics_sleeping"
    RESIDENTIAL_HOTELS_MULTIFAMILY_PRIVATE = "residential_hotels_multifamily_private"
    RESIDENTIAL_HOTELS_MULTIFAMILY_PUBLIC = "residential_hotels_multifamily_public"
    RESIDENTIAL_ONE_TWO_FAMILY_UNINHABITABLE_ATTIC_HIGH = "residential_one_two_family_uninhabitable_attic_high"
    RESIDENTIAL_ONE_TWO_FAMILY_UNINHABITABLE_ATTIC_LOW = "residential_one_two_family_uninhabitable_attic_low"
    RESIDENTIAL_OTHER_AREAS = "residential_other_areas"
    ROOFS_ASSEMBLY = "roofs_assembly"
    ROOFS_GARDENS = "roofs_gardens"
    ROOFS_ORDINARY_FLAT_PITCHED_CURVED = "roofs_ordinary_flat_pitched_curved"
    ROOFS_OTHER_OCCUPANCY = "roofs_other_occupancy"
    SCHOOL_CLASSROOMS = "school_classrooms"
    SCHOOL_CORRIDORS_ABOVE_FIRST = "school_corridors_above_first"
    SCHOOL_CORRIDORS_FIRST_FLOOR = "school_corridors_first_floor"
    SCUTTLES_SKYLIGHT_RIB_CEILING = "scuttles_skylight_rib_ceiling"
    SIDEWALKS_DRIVEWAYS_YARDS_TRUCKING = "sidewalks_driveways_yards_trucking"
    SKATING_RINKS = "skating_rinks"
    STAIRS_EXITS = "stairs_exits"
    STORAGE_HEAVY = "storage_heavy"
    STORAGE_LIGHT = "storage_light"
    STORES_RETAIL_FIRST_FLOOR = "stores_retail_first_floor"
    STORES_RETAIL_UPPER_FLOORS = "stores_retail_upper_floors"
    STORES_WHOLESALE_ALL_FLOORS = "stores_wholesale_all_floors"
    VEHICLE_BARRIERS = "vehicle_barriers"
    WALKWAYS_ELEVATED_PLATFORMS = "walkways_elevated_platforms"
    YARDS_TERRACES_PEDESTRIANS = "yards_terraces_pedestrians"


# Mapping of Use to {uniform_psf: float, concentrated_lbs: Optional[float]}
# None means no concentrated load requirement OR handled by specific section reference (no-op).
MINIMUM_LIVE_LOADS = {
    LiveLoadUse.ACCESS_FLOOR_COMPUTER: {"uniform_psf": 100.0, "concentrated_lbs": 2000.0},
    LiveLoadUse.ACCESS_FLOOR_OFFICE: {"uniform_psf": 50.0, "concentrated_lbs": 2000.0},
    LiveLoadUse.ARMORIES_DRILL_ROOMS: {"uniform_psf": 150.0, "concentrated_lbs": None},
    LiveLoadUse.ASSEMBLY_FIXED_SEATS: {"uniform_psf": 60.0, "concentrated_lbs": None},
    LiveLoadUse.ASSEMBLY_LOBBIES: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.ASSEMBLY_MOVABLE_SEATS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.ASSEMBLY_OTHER: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.ASSEMBLY_STAGES_PLATFORMS: {
        "uniform_psf": 100.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.BALCONIES_DECKS: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.BOWLING_ALLEYS: {"uniform_psf": 75.0, "concentrated_lbs": None},
    LiveLoadUse.CATWALKS: {"uniform_psf": 40.0, "concentrated_lbs": 300.0},
    LiveLoadUse.CORRIDORS_FIRST_FLOOR: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.CORRIDORS_OTHER_FLOORS: {"uniform_psf": 80.0, "concentrated_lbs": None},
    LiveLoadUse.DANCE_HALLS_BALLROOMS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.DINING_ROOMS_RESTAURANTS: {
        "uniform_psf": 100.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.ELEVATOR_MACHINE_ROOM: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.FINISH_LIGHT_FLOOR_PLATE: {
        "uniform_psf": 20.0,
        "concentrated_lbs": 200.0,
    },
    LiveLoadUse.FIRE_ESCAPES: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.FIXED_LADDER: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.GARAGES_PASSENGER_VEHICLES: {
        "uniform_psf": 40.0,
        "concentrated_lbs": 3000.0,
    },
    LiveLoadUse.GARAGES_TRUCKS_BUSES: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.GRANDSTANDS: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.GYMNASIUMS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.HANDRAILS_GUARDS: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.HELIPADS: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.HOSPITALS_CORRIDORS_ABOVE_FIRST: {
        "uniform_psf": 80.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.HOSPITALS_OPERATING_LABS: {
        "uniform_psf": 60.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.HOSPITALS_PATIENT_ROOMS: {"uniform_psf": 40.0, "concentrated_lbs": 1000.0},
    LiveLoadUse.HOTELS: {"uniform_psf": 40.0, "concentrated_lbs": None},
    LiveLoadUse.LIBRARIES_CORRIDORS_ABOVE_FIRST: {
        "uniform_psf": 80.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.LIBRARIES_READING_ROOMS: {"uniform_psf": 60.0, "concentrated_lbs": 1000.0},
    LiveLoadUse.LIBRARIES_STACK_ROOMS: {"uniform_psf": 150.0, "concentrated_lbs": 1000.0},
    LiveLoadUse.MANUFACTURING_HEAVY: {"uniform_psf": 250.0, "concentrated_lbs": 3000.0},
    LiveLoadUse.MANUFACTURING_LIGHT: {"uniform_psf": 125.0, "concentrated_lbs": 2000.0},
    LiveLoadUse.MARQUEES: {"uniform_psf": 75.0, "concentrated_lbs": None},
    LiveLoadUse.OFFICE_CORRIDORS_ABOVE_FIRST: {
        "uniform_psf": 80.0,
        "concentrated_lbs": 2000.0,
    },
    LiveLoadUse.OFFICE_LOBBIES_FIRST_FLOOR_CORRIDORS: {
        "uniform_psf": 100.0,
        "concentrated_lbs": 2000.0,
    },
    LiveLoadUse.OFFICE_OFFICES: {"uniform_psf": 50.0, "concentrated_lbs": 2000.0},
    LiveLoadUse.PENAL_CELLS: {"uniform_psf": 40.0, "concentrated_lbs": None},
    LiveLoadUse.PENAL_CORRIDORS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.PLATFORMS_ASSEMBLY: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.PUBLIC_AREAS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.PUBLIC_RESTROOMS: {"uniform_psf": 60.0, "concentrated_lbs": None},
    LiveLoadUse.RECREATIONAL_AREAS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.RESIDENTIAL_HABITABLE_ATTICS_SLEEPING: {
        "uniform_psf": 30.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.RESIDENTIAL_HOTELS_MULTIFAMILY_PRIVATE: {
        "uniform_psf": 40.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.RESIDENTIAL_HOTELS_MULTIFAMILY_PUBLIC: {
        "uniform_psf": 100.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.RESIDENTIAL_ONE_TWO_FAMILY_UNINHABITABLE_ATTIC_HIGH: {
        "uniform_psf": 20.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.RESIDENTIAL_ONE_TWO_FAMILY_UNINHABITABLE_ATTIC_LOW: {
        "uniform_psf": 10.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.RESIDENTIAL_OTHER_AREAS: {"uniform_psf": 40.0, "concentrated_lbs": None},
    LiveLoadUse.ROOFS_ASSEMBLY: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.ROOFS_GARDENS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.ROOFS_ORDINARY_FLAT_PITCHED_CURVED: {
        "uniform_psf": 20.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.ROOFS_OTHER_OCCUPANCY: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.SCHOOL_CLASSROOMS: {"uniform_psf": 40.0, "concentrated_lbs": 1000.0},
    LiveLoadUse.SCHOOL_CORRIDORS_ABOVE_FIRST: {
        "uniform_psf": 80.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.SCHOOL_CORRIDORS_FIRST_FLOOR: {
        "uniform_psf": 100.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.SCUTTLES_SKYLIGHT_RIB_CEILING: {
        "uniform_psf": 10.0,
        "concentrated_lbs": 200.0,
    },
    LiveLoadUse.SIDEWALKS_DRIVEWAYS_YARDS_TRUCKING: {
        "uniform_psf": 250.0,
        "concentrated_lbs": 8000.0,
    },
    LiveLoadUse.SKATING_RINKS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.STAIRS_EXITS: {"uniform_psf": 100.0, "concentrated_lbs": None},
    LiveLoadUse.STORAGE_HEAVY: {"uniform_psf": 250.0, "concentrated_lbs": None},
    LiveLoadUse.STORAGE_LIGHT: {"uniform_psf": 125.0, "concentrated_lbs": None},
    LiveLoadUse.STORES_RETAIL_FIRST_FLOOR: {
        "uniform_psf": 100.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.STORES_RETAIL_UPPER_FLOORS: {
        "uniform_psf": 75.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.STORES_WHOLESALE_ALL_FLOORS: {
        "uniform_psf": 125.0,
        "concentrated_lbs": 1000.0,
    },
    LiveLoadUse.VEHICLE_BARRIERS: {"uniform_psf": None, "concentrated_lbs": None},
    LiveLoadUse.WALKWAYS_ELEVATED_PLATFORMS: {
        "uniform_psf": 60.0,
        "concentrated_lbs": None,
    },
    LiveLoadUse.YARDS_TERRACES_PEDESTRIANS: {
        "uniform_psf": 100.0,
        "concentrated_lbs": None,
    },
}

# Live load categories where reduction is prohibited.
# Corresponds to Footnote 'a' in IBC 2024 Table 1607.1.
LIVE_LOAD_REDUCTION_PROHIBITED = {
    LiveLoadUse.ARMORIES_DRILL_ROOMS,
    LiveLoadUse.ASSEMBLY_FIXED_SEATS,
    LiveLoadUse.ASSEMBLY_LOBBIES,
    LiveLoadUse.ASSEMBLY_MOVABLE_SEATS,
    LiveLoadUse.ASSEMBLY_OTHER,
    LiveLoadUse.ASSEMBLY_STAGES_PLATFORMS,
    LiveLoadUse.BOWLING_ALLEYS,
    LiveLoadUse.DANCE_HALLS_BALLROOMS,
    LiveLoadUse.DINING_ROOMS_RESTAURANTS,
    LiveLoadUse.GRANDSTANDS,
    LiveLoadUse.GYMNASIUMS,
    LiveLoadUse.HELIPADS,
    LiveLoadUse.LIBRARIES_STACK_ROOMS,
    LiveLoadUse.MANUFACTURING_HEAVY,
    LiveLoadUse.MARQUEES,
    LiveLoadUse.PLATFORMS_ASSEMBLY,
    LiveLoadUse.PUBLIC_AREAS,
    LiveLoadUse.RECREATIONAL_AREAS,
    LiveLoadUse.RESIDENTIAL_HOTELS_MULTIFAMILY_PUBLIC,
    LiveLoadUse.ROOFS_ASSEMBLY,
    LiveLoadUse.ROOFS_GARDENS,
    LiveLoadUse.SIDEWALKS_DRIVEWAYS_YARDS_TRUCKING,
    LiveLoadUse.SKATING_RINKS,
    LiveLoadUse.STAIRS_EXITS,
    LiveLoadUse.STORAGE_HEAVY,
    LiveLoadUse.YARDS_TERRACES_PEDESTRIANS,
}
