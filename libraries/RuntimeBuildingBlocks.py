"""
Halo Wars Simulator
March 19th, 2024

Runtime utilities used for combining build orders into simulation runs and reporting results

"""
import math
import csv

from libraries.BaseClass import Base
from libraries.ResourceManager import ResourceManager
from libraries.BaseConstants import *


class RuntimeBuildingBlocks:
    """
    The RuntimeBuildingBlocks section is responsible for taking a build order list and simulating it properly. This
    section specifically ensures that the build orders are fed properly into the Base and other classes, will ensure
    certain build orders happened correctly, will wait if a valid build order still needs to run (waiting for resources
    or tech or building upgrades, etc) or will skip impossible build orders (not enough build slots, not enough tech,
    etc)

    Args:
        resource_manager (ResourceManager): The resource manager instance that handles the resources
        print_mode (bool): If print mode on, print out the debugging messages and more details

    """
    def __init__(self, resource_manager: ResourceManager, print_mode=True):

        self.resource_manager = resource_manager
        self.print_mode = print_mode

    def _build_order_helper(self, build_request_result: BuildResult, base: Base, order: Orders) -> BuildOrderResults:
        """
        Generic check that can be used for new build orders and a helper class for the build verifier.

        :param build_request_result: BuildResult The build result form the build
        :param base: Base: The base that is being passed on
        :return: BuildOrderResults: The results of the build order

        """
        # If build request has bene approved, then ready,
        if build_request_result == BuildResult.APPROVED:
            if self.print_mode:
                print(f"Build approved: {order}")
            return BuildOrderResults.APPROVED

        # If not enough resources, loop again until there is enough
        if build_request_result == BuildResult.NOT_ENOUGH_RESOURCES:
            # Check to ensure there are supply pads to actually make more supplies, or at least one is being built. If
            # not enough money and no supply pads, skip
            if not self.resource_manager.is_supply_pad_built_or_being_built():
                if self.print_mode:
                    print(f"Not enough resources to build, and no supply pads detected... skipping  {order}")
                return BuildOrderResults.SKIPPED

            if self.print_mode:
                print(f"WAITING for more resources to build: {order}")
            return BuildOrderResults.WAITING

        # Ensure there is enough tech level
        if build_request_result == BuildResult.NOT_ENOUGH_TECH:
            if self.print_mode:
                print(f"Not enough tech level for build order: {order}")
            return BuildOrderResults.SKIPPED

        # If the base is not upgraded enough, check if it is upgrading. If it is, loop, if not, cancel
        if build_request_result == BuildResult.BASE_NOT_UPGRADED_ENOUGH:
            if base.base_status == BaseState.UPGRADING:
                if self.print_mode:
                    print(f"WAITING for base to upgrade: {order}")
                return BuildOrderResults.WAITING
            else:
                # if not upgrading, skip this build
                if self.print_mode:
                    print(f"Skipping build order since not enough build slots: {order}")
                return BuildOrderResults.SKIPPED

        # All other scenarios, skip
        if self.print_mode:
            print(f"Edge case scenario, skipping: {order} {build_request_result}")
        return BuildOrderResults.SKIPPED

    def build_verifier(self, order: Orders, base: Base, slot: SlotNumbers) -> BuildOrderResults:
        """
        Verify that the suggested build can be done by attempting the build order. If it cannot be done, check the
        output message and determine whether to skip the command entirely, or to  wait for specific circumstances for
        it to be completed (tech level being built, more resources, supply pad being built, etc).

        Note: This method originally returned True for success or skip, and False for wait, but that got confusing, so
        implemented the BuildOrderResults APPROVED, SKIPPED, and WAITING approach which makes it much more readable.

        The build can also be PAUSED as well, which is primarily used when waiting to build a second base. This is
        different from WAITING as PAUSED has different criteria for progressing

        :param order: Orders: The Order enum that is to be performed in this build order
        :param base: Base: the base that is going to receive these orders
        :param slot: SlotNumbers: The slot on the base that is going to have the order performed on
        :return: BuildOrderResults: The final outcome of the build order, if it is Approved, waiting, skipped, etc
        """
        if order == Orders.UPGRADE_BASE:
            result = base.upgrade_base()
            # Check if the building is paused, check to ensure the temple needed flag is on or not. If it is, and not
            # is being built, this command will have to be skipped
            if result == BuildResult.PAUSED:
                # if a temple count is needed, and the building is paused, ensure a temple is being built, if so wait,
                # if not skip
                if base.temple_needed_to_clear_second_base:
                    if self.resource_manager.current_temple_count > 0:
                        return BuildOrderResults.WAITING
                    # If here, waiting for temple but no temple is being built, skip
                    else:
                        if self.print_mode:
                            print(f"temple_needed_to_clear_second_base set to TRUE but no temple being made needed for "
                                  f"subsequent base unpause, skipping: {order}")
                        return BuildOrderResults.SKIPPED

            # Check if the building is busy, if so wait for it to finish
            if result == BuildResult.BUILDING_BUSY:
                if self.print_mode:
                    print(f"Building currently busy: {order}")
                return BuildOrderResults.WAITING

            return self._build_order_helper(build_request_result=result, order=order, base=base)

        elif order == Orders.BUILD_SUPPLY_PAD:
            result = base.build_supply_pad(build_slot_name=slot.value)
            return self._build_order_helper(build_request_result=result, order=order, base=base)

        elif order == Orders.BUILD_TEMPLE:
            result = base.build_temple(build_slot_name=slot.value)

            # Check if Temple has already been built, if it has been, skip
            if result == BuildResult.ALREADY_BUILT:
                if self.print_mode:
                    print(f"Temple already built, skipping order: {order}")
                return BuildOrderResults.SKIPPED

            return self._build_order_helper(build_request_result=result, order=order, base=base)

        elif order == Orders.UPGRADE_SUPPLY_PAD:
            result = base.upgrade_supply_pad(build_slot_name=slot.value)
            # check the tech level, if a temple is being built, then wait
            if result == BuildResult.NOT_ENOUGH_TECH:
                # if there is a temple but no tech, temple is being made, wait for it
                if self.resource_manager.current_temple_count == 1:
                    if self.print_mode:
                        print(f"WAITING for temple to finish: {order}")
                    return BuildOrderResults.WAITING
                else:
                    if self.print_mode:
                        print(f"NO temple for tech level, skipping build order: {order}")
                    return BuildOrderResults.SKIPPED

            # Check if the supply pad is currently being built
            if result == BuildResult.BUILD_IN_PROGRESS:
                if self.print_mode:
                    print(f"WAITING for supply pad to finish building: {order}")
                return BuildOrderResults.WAITING

            return self._build_order_helper(build_request_result=result, order=order, base=base)

        else:
            if self.print_mode:
                print("Not selected")
            return BuildOrderResults.SKIPPED

    def run_simulation(self, build_orders: list[list], resource_amount: int, simulation_time_max: int,
                       base_list: list[Base], fine_debug=True) -> int:
        """
        The method used to execute a simulation run. Contains the main loop, which checks the build can be done, the
        build orders are approved, or skipped, updates the bases and the resource manager, checks the exit conditions,
        and has the main state machine of the game.

        :param build_orders: list[list]: Total build orders in list format
        :param resource_amount: int: Number of resources to hit before reporting results
        :param simulation_time_max: int: Maximum time for simulation to run before timeout
        :param base_list: list[Base]: List of bases currently in simulation
        :param fine_debug: bool: If the debug print out values are desired
        :return: int: The final time it took to reach the desired number of resources
        """
        # 'i' is used to increment through the build orders. Simulation time always updates
        i = 0
        simulation_time = 0
        # Main simulation loop
        while simulation_time < simulation_time_max:
            if i < len(build_orders):
                result = self.build_verifier(order=build_orders[i][0],
                                             base=build_orders[i][1],
                                             slot=build_orders[i][2])

                # If result has been approved or skipped, increment counter build order, otherwise continue
                if result == BuildOrderResults.APPROVED:
                    i += 1
                # If a build order has been permanently skipped, write over it in the report log
                elif result == BuildOrderResults.SKIPPED:
                    build_orders[i][0] = "SKIPPED"
                    i += 1

            # Update the bases every cycle
            for base in base_list:
                base.update()
            self.resource_manager.update()

            # Extra debug print output
            # print(f"Sim time: {simulation_time} {output}")

            # Check exit condition if the resources have exceeded resource amount
            if self.resource_manager.current_money >= resource_amount:
                minutes = math.floor(simulation_time / 60)

                if fine_debug:
                    print(f"FINAL: Reached {resource_amount} resources in {simulation_time} seconds or "
                          f"{minutes} minutes, {simulation_time % 60} seconds")

                if self.print_mode:
                    for base in base_list:
                        base.print_base()

                return simulation_time

            simulation_time = simulation_time + 1

        if fine_debug:
            # If at this point, simulation time has maxed out, report results
            print(f"MAX SIM TIME: Reached {resource_amount} resources in {simulation_time} seconds")
        if self.print_mode:
            for base in base_list:
                base.print_base()

    @staticmethod
    def results_to_csv(result_list: list, output_file_path: str):
        """
        Take final results in list format and output to CSV

        :param result_list: list: The final results list
        :param output_file_path: str: The path to save the output csv in string format

        """
        with open(output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Number", "Character"])  # Write header row

            for row in result_list:
                writer.writerow(row)  # Write each row of the list to the CSV

    @staticmethod
    def report_quickest_run(result_list: list):
        """
        Helper method to quickly scan the final output list and report the lowest time found.

        Special modifications have been made so that the lowest value reported has a TEMPLE, since builds without one
        typically are not as useful

        :param result_list: The final output list with seconds and bild orders that has been gathered
        """
        # Check for the quickest output.
        # Set starting lowest integer to insanely high value so it can be updated with first real value
        lowest_integer = float('inf')
        corresponding_build_order = None
        for item in result_list:
            if item[0] is not None:
                # Need to make the temple item a constant
                if "TEMPLE" in item[1]:
                    if item[0] < lowest_integer:
                        lowest_integer = item[0]
                        corresponding_build_order = item[1]

        # Final printout
        print('\n')
        print('\n')
        print('\n')
        print(f"final quickest results: {lowest_integer} seconds, orders: {corresponding_build_order}")


