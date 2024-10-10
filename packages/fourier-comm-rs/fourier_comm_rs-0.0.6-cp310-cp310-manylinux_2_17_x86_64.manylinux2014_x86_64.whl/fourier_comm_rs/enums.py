import enum
from enum import Enum

@enum.unique
class MotorType(str, Enum):
    FSA_80_20_30 = "FSA_80_20_30"
    FSA_60_17_50 = "FSA_60_17_50"
    FSA_130_7E = "FSA_130_7E"
    FSA_36B_36E = "FSA_36B_36E"
    FSA_25_08_30 = "FSA_25_08_30"
    FSA_36_14_80 = "FSA_36_14_80"
    FSA_36_11_100 = "FSA_36_11_100"

@enum.unique
class ControlMode(str, Enum):
    POSITION = "position"
    VELOCITY = "velocity"
    CURRENT = "current"
    EFFORT = "effort"
    PD = "pd"
    