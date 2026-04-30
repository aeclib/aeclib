from enum import Enum


class ConstructionType(str, Enum):
    """
    IBC 2024 Chapter 6 Construction Types.
    Defines the fire-resistance requirements for building elements.
    """

    TYPE_I_A = "I-A"
    TYPE_I_B = "I-B"
    TYPE_II_A = "II-A"
    TYPE_II_B = "II-B"
    TYPE_III_A = "III-A"
    TYPE_III_B = "III-B"
    TYPE_IV_A = "IV-A"
    TYPE_IV_B = "IV-B"
    TYPE_IV_C = "IV-C"
    TYPE_IV_HT = "IV-HT"
    TYPE_V_A = "V-A"
    TYPE_V_B = "V-B"
