"""
Halo Wars Simulator
March 19th, 2024

Base class used to contain build slots, check build conditions, upgrades, and more.

"""
from libraries.BuildSlotClasses import BuildSlot, EmptySLot, SupplyPad, Temple
from libraries.ResourceManager import ResourceManager
from libraries.BaseConstants import *


class Base:
    """
    The Base class provides attributes and methods for the HaloWars base, which contains all the build slots as well as
    methods for building on the build slots, upgrading bases, upgrading supply pads, and more

    Args:
        :param resource_manager: ResourceManager: The ResourceManager class which contains all tech and resource
                                                    collection
        :param upgrade_level: BaseLevel: The current base level, starts as empty by default but can have the base start
                                            at any level if desired.
        :param base_number: int: The identifying base number. Mostly used for debugging purposes.
        :param pause_timer: int: Used to pause the building of a base. Typically done in the beginning of a simulation
                                    to mimic the amount of time it takes to clear a base.
        :param print_mode: bool: Debugging purposes, will enable the print messages.

    """
    def __init__(self, resource_manager: ResourceManager, upgrade_level=BaseLevel.EMPTY, base_number=0, pause_timer=0,
                 temple_needed_to_clear_second_base=False,
                 print_mode=True):
        self.base_upgrade_level = upgrade_level
        self.build_timer = 0
        self.base_status = BaseState.IDLE
        self.base_number = base_number

        self.resource_manager = resource_manager
        self.build_slots = {
            1: EmptySLot(build_slot="build_slot_1", upgrade_level_needed=BaseLevel.OUTPOST),
            2: EmptySLot(build_slot="build_slot_2", upgrade_level_needed=BaseLevel.OUTPOST),
            3: EmptySLot(build_slot="build_slot_3", upgrade_level_needed=BaseLevel.OUTPOST),
            4: EmptySLot(build_slot="build_slot_4", upgrade_level_needed=BaseLevel.KEEP),
            5: EmptySLot(build_slot="build_slot_5", upgrade_level_needed=BaseLevel.KEEP),
            6: EmptySLot(build_slot="build_slot_6", upgrade_level_needed=BaseLevel.CITADEL),
            7: EmptySLot(build_slot="build_slot_7", upgrade_level_needed=BaseLevel.CITADEL),
        }

        self.build_queue = []
        self.print_mode = print_mode
        # If there is a pause timer, put the base into the paused state
        self.pause_timer = pause_timer
        if self.pause_timer > 0:
            self.base_status = BaseState.PAUSED

        # This flag determines if building a temple is needed to un-pause the pause countdown timer
        # The thought process is if the pause is tied to the player using their prophet to clear a base themselves,
        # which is relative to when the temple is built, or if a teammate will clear a base for them (TRUE), which is
        # not relative to the temple being made (FALSE)
        self.temple_needed_to_clear_second_base = temple_needed_to_clear_second_base

    def _default_build_slot_check(self, build_slot_name: int, tech_requirement: int, resource_requirement: int,
                                  building_to_build: BuildSlot) -> BuildResult:
        """
        Method that can do some basic checks before making a build slot, things like resource and tech requirements as
        well as checking if a slot has already been built.

        Note, if approved, this method will subtract the resources from the desired location.

        :param build_slot_name: str: The name of the corresponding build slot to build on
        :param tech_requirement: int: The tech level needed for the building to be built
        :param resource_requirement: int: the amount of resources needed in order to build the building
        :return: BuildResult: The build result from attempting to build the building

        """
        # Check if the build slot exists, if not return error
        if build_slot_name not in self.build_slots:
            if self.print_mode:
                print(f"Desired build slot does not exist")
            return BuildResult.BASE_NOT_UPGRADED_ENOUGH

        # Ensure the build slot is empty
        if self.build_slots[build_slot_name].build_type != BuildSlotType.EMTPY:
            if self.print_mode:
                print(f"Build slot {build_slot_name} is not empty for new building")
            return BuildResult.ALREADY_BUILT

        # Ensure the base upgrade level is high enough for the slot that wants to be built, otherwise exit
        if self.base_upgrade_level.value < self.build_slots.get(build_slot_name).upgrade_level_needed.value:
            if self.print_mode:
                print(f"Base is not upgraded enough to build there")
            return BuildResult.BASE_NOT_UPGRADED_ENOUGH

        # Ensure the proper tech level is ready
        if tech_requirement > self.resource_manager.current_tech_level:
            if self.print_mode:
                print(f"Tech level for desired building is not high enough")
            return BuildResult.NOT_ENOUGH_TECH

        # Ensure the correct amount of money is available and subtract it
        if self.resource_manager.subtract_money(resource_requirement):
            self.build_slots[build_slot_name] = building_to_build
            self.build_slots[build_slot_name].build()
            self.build_queue.append(self.build_slots[build_slot_name])
            return BuildResult.APPROVED
        else:
            if self.print_mode:
                print(f"Not enough resources to build: {build_slot_name}")
            return BuildResult.NOT_ENOUGH_RESOURCES

    def build_supply_pad(self, build_slot_name: int) -> BuildResult:
        """
        Helper method that will build a supply pad at dedicated build slot on base. Calls _default_build_slot_check to
        ensure that the slot can be built accordingly. If it fails, will return specific error code.

        :param build_slot_name: str: The slot location on the base to build
        :return: BuildResult: The result from the build attempt in the BuildResult class

        """
        build_result = self._default_build_slot_check(build_slot_name=build_slot_name,
                                                      tech_requirement=0,
                                                      resource_requirement=SUPPLY_PAD_COST,
                                                      building_to_build=SupplyPad(resource_manager=self.resource_manager,
                                                                                  build_slot=build_slot_name,
                                                                                  print_mode=self.print_mode))

        if self.print_mode:
            print(f"Supply pad build {build_result}: {build_slot_name}")
        return build_result

    def build_temple(self, build_slot_name: int) -> BuildResult:
        """
        Helper method that will build a Temple at dedicated build slot on base. Calls the _default_build_slot_check
        method to ensure the build can happen. Also ensures that no other temples have been built before performing the
        check.

        :param build_slot_name: str: The slot location on the base to build
        :return: BuildResult: The result from the build attempt in the BuildResult class

        """
        # Check if temple has already been built, if it has, return with an ALREADY_BUILT status
        if self.resource_manager.current_temple_count > 0:
            if self.print_mode:
                print(f"Temple already built {build_slot_name}")
            return BuildResult.ALREADY_BUILT

        build_result = self._default_build_slot_check(build_slot_name=build_slot_name,
                                                      tech_requirement=0,
                                                      resource_requirement=TEMPLE_COST,
                                                      building_to_build=Temple(resource_manager=self.resource_manager,
                                                                               build_slot=build_slot_name,
                                                                               print_mode=self.print_mode))
        if self.print_mode:
            print(f"Temple Build {build_result}: {build_slot_name}")
        return build_result

    def upgrade_supply_pad(self, build_slot_name: int) -> BuildResult:
        """
        Upgrade the listed supply pad. Before doing that, perform several checks to ensure the supply pad is in the
        right state and is ready for an upgrade.

        :param build_slot_name: str: The slot that wishes to get upgraded
        :return: BuildResult: The final result from the attempted build/upgrade

        """
        # Check if the build slot exists, if not return error
        if build_slot_name not in self.build_slots:
            if self.print_mode:
                print(f"Desired build slot does not exist")
            return BuildResult.BASE_NOT_UPGRADED_ENOUGH

        # Ensure the build slot is a supply pad
        if self.build_slots[build_slot_name].build_type != BuildSlotType.SUPPLY_PAD:
            if self.print_mode:
                print(f"Not a Supply Pad: {build_slot_name}")
            return BuildResult.NOT_A_SUPPLY_PAD

        # Ensure supply pad is BUILT and not being built or any other stages
        if self.build_slots[build_slot_name].status == BuildSlotState.UPGRADED:
            if self.print_mode:
                print(f"Supply Pad already upgraded: {build_slot_name}")
            return BuildResult.SUPPLY_PAD_ALREADY_UPGRADED
        elif self.build_slots[build_slot_name].status == BuildSlotState.BUILDING:
            if self.print_mode:
                print(f"Supply Pad building in progress: {build_slot_name}")
            return BuildResult.BUILD_IN_PROGRESS
        elif self.build_slots[build_slot_name].status == BuildSlotState.UPGRADING:
            if self.print_mode:
                print(f"Supply Pad already upgrading: {build_slot_name}")
            return BuildResult.SUPPLY_PAD_ALREADY_UPGRADED
        elif self.build_slots[build_slot_name].status != BuildSlotState.BUILT:
            if self.print_mode:
                print(f"Supply pad not built: {build_slot_name}")
            return BuildResult.BUILDING_NOT_BUILT

        # Check the tech level
        if self.resource_manager.current_tech_level < 1:
            if self.print_mode:
                print(f"Not high enough tech to upgrade supply pad: {build_slot_name}")
            return BuildResult.NOT_ENOUGH_TECH

        # Check the money situation and approve if good!
        if self.resource_manager.subtract_money(SUPPLY_PAD_UPGRADE_COST):
            self.build_slots[build_slot_name].upgrade()
            self.build_queue.append(self.build_slots[build_slot_name])
            if self.print_mode:
                print(f"Supply Pad upgrade APPROVED: {build_slot_name}")
            return BuildResult.APPROVED
        else:
            if self.print_mode:
                print(f"Not enough money to upgrade supply pad: {build_slot_name}")
            return BuildResult.NOT_ENOUGH_RESOURCES

    def _base_upgrade_helper(self, upgrade_cost: int, upgrade_timer: int) -> BuildResult:
        """
        Helper function for building and upgrading a base. Ensures the build checks are all consistent across all base
        upgrades and builds.

        :param upgrade_cost: int: The cost for the build/upgrade
        :param upgrade_timer: int: How long the build/upgrade should take
        :return: BuildResult: The result from the attempted build

        """
        # check if there is enough money, if so, approve
        if self.resource_manager.subtract_money(upgrade_cost):
            if self.print_mode:
                print(f"Building {BaseLevel(self.base_upgrade_level.value + 1)}")
            self.base_status = BaseState.UPGRADING
            self.build_timer = upgrade_timer
            return BuildResult.APPROVED
        else:
            if self.print_mode:
                print(f"Not enough resources for {BaseLevel(self.base_upgrade_level.value + 1)}")
            return BuildResult.NOT_ENOUGH_RESOURCES

    def upgrade_base(self) -> BuildResult:
        """
        Does a series of checks and upgrades the base based on what state its in and if it meets the requirements.

        :return: BuildResult: The final result from the attempted Base build/upgrade

        """
        # If the base state is paused, return that
        if self.base_status == BaseState.PAUSED:
            if self.print_mode:
                print(f"Base {self.base_number} is currently PAUSED")
            return BuildResult.PAUSED

        # Ensure the base is in an IDLE state, otherwise cant upgrade
        if self.base_status != BaseState.IDLE:
            if self.print_mode:
                print(f"Base {self.base_number} state is not idle, currently {self.base_status}")
            return BuildResult.BUILDING_BUSY

        # Check if base is a CITIDALE, in which case already max level, skip
        if self.base_upgrade_level == BaseLevel.CITADEL:
            if self.print_mode:
                print("already max level")
            return BuildResult.ALREADY_BUILT

        # Perform the checks for each base upgrade level
        if self.base_upgrade_level == BaseLevel.EMPTY:
            return self._base_upgrade_helper(upgrade_cost=BASE_BUILD_COST,
                                             upgrade_timer=BASE_BUILD_TIME_SECONDS)
        elif self.base_upgrade_level == BaseLevel.OUTPOST:
            return self._base_upgrade_helper(upgrade_cost=KEEP_UPGRADE_COST,
                                             upgrade_timer=KEEP_UPGRADE_TIME_SECONDS)
        elif self.base_upgrade_level == BaseLevel.KEEP:
            return self._base_upgrade_helper(upgrade_cost=CITADEL_UPGRADE_COST,
                                             upgrade_timer=CITADEL_UPGRADE_TIME_SECONDS)
        else:
            if self.print_mode:
                print("Invalid Base level")
            return BuildResult.ERROR

    def update(self):
        """
        Update logic that runs every game tick. Updates the counters for upgrades, builds and more.

        """
        # If the base is IDLE, then not paused or upgrading, so start updating slots
        if self.base_status == BaseState.IDLE:
            # Check the build queue. If it is not 0, then start updating.
            if len(self.build_queue) > 0:
                # If the state is IDLE, then it hasnt been started, set state to BUILDING
                if self.build_queue[0].status == BuildSlotState.IDLE:
                    self.build_queue[0].status = BuildSlotState.BUILDING
                # If the state is no longer building, and not IDLE, then must be DONE or UPGRADED, so can remove.
                elif self.build_queue[0].status is not BuildSlotState.BUILDING:
                    self.build_queue.pop(0)
            # Update each build slot
            for slot_name in self.build_slots:
                self.build_slots[slot_name].update()

        # Check the build timer. If > 0 then base is building/upgrading. and increment.
        elif self.base_status == BaseState.UPGRADING:
            if self.build_timer > 0:
                self.build_timer = self.build_timer - 1
            else:
                # If the state of the base was UPGRADING but no build timer, then the base has been upgraded, increment.
                current_index = self.base_upgrade_level.value
                if current_index < len(BaseLevel) - 1:
                    next_level_index = current_index + 1
                    self.base_upgrade_level = BaseLevel(next_level_index)
                self.base_status = BaseState.IDLE
                if self.print_mode:
                    print(f"BASE UPGRADED: IS NOW {self.base_upgrade_level}, {self.base_status}")
                self.build_timer = 0

        # Check the pause timer. The pause timer is used for things like simulating clearing a base, where the base
        # is not immediately available build
        elif self.base_status == BaseState.PAUSED:
            # if a temple is required, then check if there is a tech level, which notes a temple has been built, which
            # means a prophet is out and the base clearing countdown can continue
            if self.temple_needed_to_clear_second_base:
                if self.resource_manager.current_tech_level <= 0:
                    # If at this point, not tech level, skip
                    return

            # If have gotten through the temple needed check, decrement timer
            if self.pause_timer > 0:
                self.pause_timer -= 1
            else:
                self.base_status = BaseState.IDLE
                if self.print_mode:
                    print(f"BASE is no longer paused: IS NOW {self.base_status}")
                self.pause_timer = 0

    def print_base(self):
        """
        Print base info and build slots on the base. Can be used to print other information about the base as well.

        """
        print("--- Base print --- ")
        print(f"Base number: {self.base_number}")
        print(f"Base level : {self.base_upgrade_level}")
        print(f"Base status: {self.base_status}")
        for slot_name in self.build_slots:
            print("  - " + self.build_slots[slot_name].name + " " + str(self.build_slots[slot_name].status))

    # ----------------------------------------------------------------
    # Helper functions below
    # ----------------------------------------------------------------

    def is_supply_pad_built(self, build_slot_name: int) -> bool:
        """
        Helper function to check is supply pad has been built.

        :param build_slot_name: str: Name of build slot to check
        :return: bool: True if supply pad has been built, false if not
        """
        # Check if there's an available build slot
        if build_slot_name in self.build_slots:
            if self.build_slots[build_slot_name].build_type == BuildSlotType.SUPPLY_PAD:
                if (self.build_slots[build_slot_name].status == BuildSlotState.BUILT or
                        self.build_slots[build_slot_name].status == BuildSlotState.UPGRADED):
                    return True
                else:
                    return False

    def is_supply_pad_upgraded(self, build_slot_name: int) -> bool:
        """
        Helper function to check if specified supply pad is upgraded.

        :param build_slot_name: str: Name of build slot to check
        :return: bool: True if supply pad is upgraded, false if not
        """
        if build_slot_name in self.build_slots:
            if self.build_slots[build_slot_name].build_type == BuildSlotType.HEAVY_SUPPLY_PAD:
                return True
            else:
                return False

    def get_next_build_cost(self) -> int:
        """
        Helper function that can get the next build cost for the base.

        :return: int: the cost of the next base build
        """
        if self.base_upgrade_level == BaseLevel.EMPTY:
            return BASE_BUILD_COST
        elif self.base_upgrade_level == BaseLevel.OUTPOST:
            return KEEP_UPGRADE_COST
        elif self.base_upgrade_level == BaseLevel.KEEP:
            return CITADEL_UPGRADE_COST
        else:
            if self.print_mode:
                print("not an option for get_next_build_cost")
