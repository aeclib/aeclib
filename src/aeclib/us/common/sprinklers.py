from enum import Enum


class SprinklerSystem(str, Enum):
    """
    IBC 2024 Sprinkler System Types.
    Crucial for allowable height and area calculations.
    """

    NOT_SPRINKLERED = "NS"
    FULLY_SPRINKLERED = "S"  # NFPA 13 (Section 903.3.1.1)
    SPRINKLERED_13R = "S13R"  # NFPA 13R (Section 903.3.1.2)
    SPRINKLERED_13D = "S13D"  # NFPA 13D (Section 903.3.1.3)
