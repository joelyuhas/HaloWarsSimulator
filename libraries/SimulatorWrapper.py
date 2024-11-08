"""
Halo Wars Simulator
March 19th, 2024

Simulation Wrapper to take care of setting up a simulation for the user with all the correct objects and defaults.

"""
from libraries.BaseClass import Base
from libraries.ResourceManager import ResourceManager
from libraries.BaseConstants import BaseLevel
from libraries.RuntimeBuildingBlocks import RuntimeBuildingBlocks


class SimulatorWrapper:
    """
    This class is a basic wrapper used for instantiating everything needed to run a basic simulation. The idea is that
    this wrapper will take care of all the nuts and bolts instantiations and allow a more simplified interface for
    setting up the simulations without missing any steps if not desired.

    Ultimately, Takes care of all the nitty gritty with setting up a simulation, and keeps track of specific objects,
    like the ResourceManger, base list, debug modes,etc.

    """
    def __init__(self, starting_money: int, debug_mode=False, fine_debug=True):
        self.resource_manager = ResourceManager()
        self.resource_manager.add_money(starting_money)
        self.debug_mode = debug_mode
        self.fine_debug = fine_debug
        self.runtime_building_blocks = RuntimeBuildingBlocks(resource_manager=self.resource_manager,
                                                             print_mode=debug_mode)
        self.base_list = []

    def add_base(self, upgrade_level: BaseLevel, base_number: int):
        """
        Method to add a base to the simulation, to add before running the simulation. This is its own method since
        different bases and a different number of bases can be added later with different properties.

        :param upgrade_level: BaseLevel: Starting level of the base
        :param base_number: int: Base identification number
        """
        base_to_add = Base(resource_manager=self.resource_manager,
                           upgrade_level=upgrade_level,
                           print_mode=self.debug_mode,
                           base_number=base_number)

        self.base_list.append(base_to_add)

    def run_simulation(self, build_order: list, resource_trigger: int, simulation_time_seconds: int) -> int:
        """
        Used to run the simulation. Primarily, provides the base list and debug attributes for the user.

        :param build_order: list: Builds to execute in the simulation
        :param resource_trigger: int: The amount of resources to reach the exit scenario
        :param simulation_time_seconds: int: Maximum time for the simulation to reach
        :return: int: The final number of seconds it took to reach the designated amount of resources
        """
        # Run the actual simulation
        final_sim_time = self.runtime_building_blocks.run_simulation(build_orders=build_order,
                                                                     resource_amount=resource_trigger,
                                                                     simulation_time_max=simulation_time_seconds,
                                                                     base_list=self.base_list,
                                                                     fine_debug=self.fine_debug)
        return final_sim_time


