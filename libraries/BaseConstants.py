"""
Halo Wars Simulator
March 19th, 2024

Constants used from state machine enums to resource costs to build times

"""
from enum import Enum

# The starting money used by default
STARTING_MONEY = 800


# Base build and upgrade times
BASE_BUILD_TIME_SECONDS = 30
KEEP_UPGRADE_TIME_SECONDS = 15
CITADEL_UPGRADE_TIME_SECONDS = 30


# Build slot specific build and upgrade resource costs
SUPPLY_PAD_COST = 100
SUPPLY_PAD_UPGRADE_COST = 225
TEMPLE_COST = 500

# Build slot build/upgrade times
TEMPLE_BUILD_TIME_SECONDS = 30
SUPPLY_PAD_BUILD_TIME_SECONDS = 30
SUPPLY_PAD_UPGRADE_TIME_SECONDS = 17.5

# Base bild and upgrade costs
BASE_BUILD_COST = 500
KEEP_UPGRADE_COST = 300
CITADEL_UPGRADE_COST = 400


# After a build order has been done, the results for the RuntimeBuildingBlocks are used to determine what state its in
class BuildOrderResults(Enum):
    APPROVED = 0
    SKIPPED = 1
    WAITING = 2
    DENIED = 3


# Slot types currently available for a build slot
class BuildSlotType(Enum):
    EMTPY = 0
    SUPPLY_PAD = 1
    HEAVY_SUPPLY_PAD = 2
    TEMPLE = 3


# The state in the build slot state machine
class BuildSlotState(Enum):
    IDLE = 0
    BUILDING = 1
    BUILT = 2
    UPGRADING = 3
    UPGRADED = 4


# The states the Base can be in the base state machine
class BaseState(Enum):
    EMPTY = 0
    IDLE = 1
    UPGRADING = 2
    PAUSED = 3


# The Base's level
class BaseLevel(Enum):
    EMPTY = 0
    OUTPOST = 1
    KEEP = 2
    CITADEL = 3


# After a build requested has been executed, the following are the results of what can happen
class BuildResult(Enum):
    APPROVED = 0
    ALREADY_BUILT = 1
    NOT_ENOUGH_RESOURCES = 2
    NOT_ENOUGH_TECH = 3
    NOT_A_SUPPLY_PAD = 4
    BUILDING_NOT_BUILT = 5
    SUPPLY_PAD_ALREADY_UPGRADED = 6
    BUILD_IN_PROGRESS = 7
    BASE_NOT_UPGRADED_ENOUGH = 8
    BUILDING_BUSY = 9
    PAUSED = 10
    ERROR = 11


# The build orders that can happen
class Orders(Enum):
    BUILD_SUPPLY_PAD = 1
    BUILD_TEMPLE = 2
    UPGRADE_BASE = 3  # also build base cost
    UPGRADE_SUPPLY_PAD = 4


# The slot numbers available on a base
class SlotNumbers(Enum):
    build_slot_1 = 1
    build_slot_2 = 2
    build_slot_3 = 3
    build_slot_4 = 4
    build_slot_5 = 5
    build_slot_6 = 6
    build_slot_7 = 7


def get_slot_number(int_value: int) -> SlotNumbers:
    """
    Helper method to get the slot number of a specific int value.

    :param int_value: int: The integer value provided
    :return: The corresponding slot number
    :raises: ValueError: If the slot number provided is not in the list
    """
    for slot_number in SlotNumbers:
        if slot_number.value == int_value:
            return slot_number
    # if at this point, slot value is out of range
    raise ValueError(f"Invalid slot number provided, or out of range: {int_value}")

