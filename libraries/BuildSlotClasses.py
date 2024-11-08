"""
Halo Wars Simulator
March 19th, 2024

Build Slots used for designating and defining what buildings can be made in build slots.

"""
from abc import ABC, abstractmethod


from libraries.ResourceManager import ResourceManager
from libraries.BaseConstants import BaseLevel, BuildSlotState, BuildSlotType, SUPPLY_PAD_UPGRADE_COST, SUPPLY_PAD_COST, \
    SUPPLY_PAD_UPGRADE_TIME_SECONDS, SUPPLY_PAD_BUILD_TIME_SECONDS, TEMPLE_BUILD_TIME_SECONDS


class BuildSlot(ABC):
    """
    Parent BuildSlot class which all other slots inherit from. Sets up the foundation for the other build slot classes

    Args:
        build_slot (int): Corresponding build slot string/number identification/base position location
        resource_manager (ResourceManager): The resource manager instance used for modifying resource and tech levels
        status (BuildSlotState): Current status of the slot based on the slot state machine
        build_timer (int): Current build timer for specific slot
        build_type (BuildSlotType): They build type that this slot is
        print_mode (bool): Will print debug print  statements
        name (str): Build slot name. Used for printing.

    """
    def __init__(self, resource_manager: ResourceManager, build_slot: int, print_mode: bool = True):
        self.build_slot = build_slot
        self.resource_manager = resource_manager
        self.status = BuildSlotState.IDLE
        self.build_timer = 0
        self.build_type = BuildSlotType.EMTPY
        self.print_mode = print_mode
        self.name = "build_slot"

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def update(self):
        pass


class EmptySLot(BuildSlot):
    """
    The Empty slot is the default/starting slot. This is used to let other programs know the slot is empty and can be
    used to build new slots.

    No resource manager is needed.
    """
    def __init__(self, build_slot: str, upgrade_level_needed: BaseLevel):
        super().__init__(resource_manager=None, build_slot=build_slot, print_mode=None)
        self.build_type = BuildSlotType.EMTPY
        self.upgrade_level_needed = upgrade_level_needed
        self.name = "EMPTY_SLOT"

    def build(self):
        pass

    def update(self):
        pass

    def get_type(self):
        return BuildSlotType


class Temple(BuildSlot):
    """
    Temple is the build slot that upgrades the base tech level.

    """
    def __init__(self, resource_manager: ResourceManager, build_slot, print_mode=True):
        super().__init__(resource_manager=resource_manager, build_slot=build_slot, print_mode=print_mode)
        self.name = "TEMPLE    "  # Note, spacing is used for formatting reasons when printing

    def build(self):
        """
        Perform the build operation for adding a temple. Add the temple to the resource manager right away to signify
        a temple is being constructed. The tech level won't increase until after the temple is complete.

        """
        self.status = BuildSlotState.IDLE
        self.build_timer = TEMPLE_BUILD_TIME_SECONDS
        self.resource_manager.add_temple()
        if self.print_mode:
            print(f"Building Temple...: {self.build_slot}")

    def update(self):
        """
        Update is used to update the temple contents/values every game cycle. Specifically, update the timers, tech
        levels, etc.

        """
        if self.status == BuildSlotState.IDLE:
            pass
        elif self.status == BuildSlotState.BUILDING:
            # If the timer is larger than 0, building is being built, subtract from timer
            if self.build_timer > 0:
                self.build_timer = self.build_timer - 1

            # If not IDLE or BUILDING, then the temple has been built, add it to the resource manger and change status
            else:
                if self.print_mode:
                    print(f"Temple complete: {self.build_slot}")
                self.resource_manager.add_tech_level()
                self.status = BuildSlotState.BUILT
                self.build_timer = 0


class SupplyPad(BuildSlot):
    """
    Supply pad adds supplies at a specific rate to the resource manager.
    """
    def __init__(self, resource_manager: ResourceManager, build_slot: int, print_mode=True):
        super().__init__(resource_manager=resource_manager, build_slot=build_slot, print_mode=print_mode)
        self.build_type = BuildSlotType.SUPPLY_PAD
        self.name = "SUPPLY_PAD"

    def build(self):
        """
        Perform the build operation for adding a supply pad.

        """
        self.status = BuildSlotState.IDLE
        self.build_timer = SUPPLY_PAD_BUILD_TIME_SECONDS
        # Note that a supply pad is being built. Used for checking status of supply pad
        self.resource_manager.note_supply_pad_is_being_built()
        if self.print_mode:
            print(f"Building Supply Pad...: {self.build_slot}")

    def upgrade(self):
        """
        Upgrade an already built supply pad. This causes the supply pad to produce more supplies. Requires at-least 1
        tech level.

        """
        if self.resource_manager.current_tech_level >= 1:
            if self.print_mode:
                print(f"Upgrading Supply Pad...: {self.build_slot}")
            self.status = BuildSlotState.UPGRADING
            self.build_timer = SUPPLY_PAD_UPGRADE_TIME_SECONDS
        else:
            if self.print_mode:
                print(f"Not high enough tech level {self.build_slot}")

    def update(self):
        """
        Update loop for the supply pad. If IDLE do nothing, but if BUILDING or UPGRADENg check the build timer.

        """
        if self.status == BuildSlotState.IDLE:
            pass
        elif self.status == BuildSlotState.BUILDING or self.status == BuildSlotState.UPGRADING:
            if self.build_timer > 0:
                self.build_timer = self.build_timer - 1
            else:
                # When the timer is 0 and still in BUILDING state, that means build is done. Change state and add
                if self.status == BuildSlotState.BUILDING:
                    self.status = BuildSlotState.BUILT
                    self.resource_manager.add_lite_supply_pad()
                    if self.print_mode:
                        print(f"Supply pad complete: {self.build_slot}")
                # When the timer is 0 and still in UPGRADING state, that means build is done. Change state and add
                elif self.status == BuildSlotState.UPGRADING:
                    self.status = BuildSlotState.UPGRADED
                    self.resource_manager.add_heavy_supply_pad()
                    self.resource_manager.remove_lite_supply_pad()
                    self.build_type = BuildSlotType.HEAVY_SUPPLY_PAD
                    if self.print_mode:
                        print(f"Supply pad upgraded: {self.build_slot}")
                self.build_timer = 0





