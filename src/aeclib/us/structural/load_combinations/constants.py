from enum import Enum


class DesignMethod(str, Enum):
    """Supported design methods for load combinations."""

    ASD = "ASD"
    LRFD = "LRFD"
    BOTH = "both"


# LRFD Load Combination Templates (ASCE 7-16 Section 2.3)
LRFD_TEMPLATES = [
    ("LRFD_1", "1.4D", {"dead": 1.4}),
    ("LRFD_2_Lr", "1.2D + 1.6L + 0.5Lr", {"dead": 1.2, "live": 1.6, "roof_live": 0.5}),
    ("LRFD_2_S", "1.2D + 1.6L + 0.5S", {"dead": 1.2, "live": 1.6, "snow": 0.5}),
    ("LRFD_2_R", "1.2D + 1.6L + 0.5R", {"dead": 1.2, "live": 1.6, "rain": 0.5}),
    ("LRFD_3_Lr_L", "1.2D + 1.6Lr + 1.0L", {"dead": 1.2, "roof_live": 1.6, "live": 1.0}),
    ("LRFD_3_Lr_W_pos", "1.2D + 1.6Lr + 0.5W", {"dead": 1.2, "roof_live": 1.6, "wind": 0.5}),
    ("LRFD_3_Lr_W_neg", "1.2D + 1.6Lr - 0.5W", {"dead": 1.2, "roof_live": 1.6, "wind": -0.5}),
    ("LRFD_3_S_L", "1.2D + 1.6S + 1.0L", {"dead": 1.2, "snow": 1.6, "live": 1.0}),
    ("LRFD_3_S_W_pos", "1.2D + 1.6S + 0.5W", {"dead": 1.2, "snow": 1.6, "wind": 0.5}),
    ("LRFD_3_S_W_neg", "1.2D + 1.6S - 0.5W", {"dead": 1.2, "snow": 1.6, "wind": -0.5}),
    ("LRFD_3_R_L", "1.2D + 1.6R + 1.0L", {"dead": 1.2, "rain": 1.6, "live": 1.0}),
    ("LRFD_3_R_W_pos", "1.2D + 1.6R + 0.5W", {"dead": 1.2, "rain": 1.6, "wind": 0.5}),
    ("LRFD_3_R_W_neg", "1.2D + 1.6R - 0.5W", {"dead": 1.2, "rain": 1.6, "wind": -0.5}),
    ("LRFD_4_Lr_pos", "1.2D + 1.0W + 1.0L + 0.5Lr", {"dead": 1.2, "wind": 1.0, "live": 1.0, "roof_live": 0.5}),
    ("LRFD_4_Lr_neg", "1.2D - 1.0W + 1.0L + 0.5Lr", {"dead": 1.2, "wind": -1.0, "live": 1.0, "roof_live": 0.5}),
    ("LRFD_4_S_pos", "1.2D + 1.0W + 1.0L + 0.5S", {"dead": 1.2, "wind": 1.0, "live": 1.0, "snow": 0.5}),
    ("LRFD_4_S_neg", "1.2D - 1.0W + 1.0L + 0.5S", {"dead": 1.2, "wind": -1.0, "live": 1.0, "snow": 0.5}),
    ("LRFD_4_R_pos", "1.2D + 1.0W + 1.0L + 0.5R", {"dead": 1.2, "wind": 1.0, "live": 1.0, "rain": 0.5}),
    ("LRFD_4_R_neg", "1.2D - 1.0W + 1.0L + 0.5R", {"dead": 1.2, "wind": -1.0, "live": 1.0, "rain": 0.5}),
    ("LRFD_5_pos", "1.2D + 1.0E + 1.0L + 0.2S", {"dead": 1.2, "seismic": 1.0, "live": 1.0, "snow": 0.2}),
    ("LRFD_5_neg", "1.2D - 1.0E + 1.0L + 0.2S", {"dead": 1.2, "seismic": -1.0, "live": 1.0, "snow": 0.2}),
    ("LRFD_6_pos", "0.9D + 1.0W", {"dead": 0.9, "wind": 1.0}),
    ("LRFD_6_neg", "0.9D - 1.0W", {"dead": 0.9, "wind": -1.0}),
    ("LRFD_7_pos", "0.9D + 1.0E", {"dead": 0.9, "seismic": 1.0}),
    ("LRFD_7_neg", "0.9D - 1.0E", {"dead": 0.9, "seismic": -1.0}),
]

# ASD Load Combination Templates (ASCE 7-16 Section 2.4)
ASD_TEMPLATES = [
    ("ASD_1", "D", {"dead": 1.0}),
    ("ASD_2", "D + L", {"dead": 1.0, "live": 1.0}),
    ("ASD_3_Lr", "D + Lr", {"dead": 1.0, "roof_live": 1.0}),
    ("ASD_3_S", "D + S", {"dead": 1.0, "snow": 1.0}),
    ("ASD_3_R", "D + R", {"dead": 1.0, "rain": 1.0}),
    ("ASD_4_Lr", "D + 0.75L + 0.75Lr", {"dead": 1.0, "live": 0.75, "roof_live": 0.75}),
    ("ASD_4_S", "D + 0.75L + 0.75S", {"dead": 1.0, "live": 0.75, "snow": 0.75}),
    ("ASD_4_R", "D + 0.75L + 0.75R", {"dead": 1.0, "live": 0.75, "rain": 0.75}),
    ("ASD_5_W_pos", "D + 0.6W", {"dead": 1.0, "wind": 0.6}),
    ("ASD_5_W_neg", "D - 0.6W", {"dead": 1.0, "wind": -0.6}),
    ("ASD_5_E_pos", "D + 0.7E", {"dead": 1.0, "seismic": 0.7}),
    ("ASD_5_E_neg", "D - 0.7E", {"dead": 1.0, "seismic": -0.7}),
    ("ASD_6_Lr_pos", "D + 0.75L + 0.45W + 0.75Lr", {"dead": 1.0, "live": 0.75, "wind": 0.45, "roof_live": 0.75}),
    ("ASD_6_Lr_neg", "D + 0.75L - 0.45W + 0.75Lr", {"dead": 1.0, "live": 0.75, "wind": -0.45, "roof_live": 0.75}),
    ("ASD_6_S_pos", "D + 0.75L + 0.45W + 0.75S", {"dead": 1.0, "live": 0.75, "wind": 0.45, "snow": 0.75}),
    ("ASD_6_S_neg", "D + 0.75L - 0.45W + 0.75S", {"dead": 1.0, "live": 0.75, "wind": -0.45, "snow": 0.75}),
    ("ASD_6_R_pos", "D + 0.75L + 0.45W + 0.75R", {"dead": 1.0, "live": 0.75, "wind": 0.45, "rain": 0.75}),
    ("ASD_6_R_neg", "D + 0.75L - 0.45W + 0.75R", {"dead": 1.0, "live": 0.75, "wind": -0.45, "rain": 0.75}),
    ("ASD_7_pos", "D + 0.75L + 0.525E + 0.75S", {"dead": 1.0, "live": 0.75, "seismic": 0.525, "snow": 0.75}),
    ("ASD_7_neg", "D + 0.75L - 0.525E + 0.75S", {"dead": 1.0, "live": 0.75, "seismic": -0.525, "snow": 0.75}),
    ("ASD_8_pos", "0.6D + 0.6W", {"dead": 0.6, "wind": 0.6}),
    ("ASD_8_neg", "0.6D - 0.6W", {"dead": 0.6, "wind": -0.6}),
    ("ASD_9_pos", "0.6D + 0.7E", {"dead": 0.6, "seismic": 0.7}),
    ("ASD_9_neg", "0.6D - 0.7E", {"dead": 0.6, "seismic": -0.7}),
]
