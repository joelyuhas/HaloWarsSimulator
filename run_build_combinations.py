"""
Halo Wars Simulator
March 19th, 2024

Main executable for generating random build orders and running simulations against them

"""
from libraries.BaseConstants import BaseLevel
from libraries.GenerateOrdersBuildingBlocks import GenerateOrdersBuildingBlocks
from libraries.RuntimeBuildingBlocks import RuntimeBuildingBlocks
from libraries.SimulatorWrapper import SimulatorWrapper

# Toggle debug mode. When true, all print statements will be turned on. Off for faster runtimes
DEBUG_MODE = False
# Fine debug mode will toggle printing the final print on the end of every run. Toggle off if doing very long runs
FINE_DEBUG = False
# The amount of money to start with, default is 800
STARTING_RESOURCES = 800
# The timeout for each individual simulated run that the run will exit if reaches, in-game SECONDS
SIMULATION_TIME_SECONDS = 1000
# Goal amount of resources to reach to exit simulation and report findings
RESOURCE_TRIGGER_VALUE = 3000
# Number of bases to perform simulation with. Can be 1 to as many as wanted
NUMBER_OF_BASES = 2
# How many simulations should be run. 100 for 100 different iterations, etc
NUMBER_OF_SIMULATION_LOOPS = 200
# If no Temple is listed in final results, remove it if enabled
REMOVE_IF_NO_TEMPLE = True
# Second base pause timer, used to mimic the amount of time it would take to clear a second base. Not needed on Exile,
# but could consider a 7-second pause on exile since that's how long it takes to get to the new base. Set to 0 to
# disable
SUBSEQUENT_BASE_PAUSE_TIMER_SECONDS = 120
# If a temple is required to start the pause timer. This is typically toggled TRUE if it is being simulated that the
# player is clearing their own base (they need a temple which produces a prophet to clear the base, so second base timer
# doesnt start until AFTER a temple has been made), or this is toggled to FALSE if its expected another teammate will
# clear the second base, in which case the temple order is irrelevant as the other teammate will do the job of base
# clearing. In that scenario, the second base pause timer starts right away
IS_TEMPLE_REQUIRED_TO_START_PAUSE_TIMER = True


def main():
    """
    The run_build_combinations file is the main executable for running and finding random build combination values.

    This files primary purpose is to generate X amount of random build orders, simulate them using the halo wars
    simulator, and report the time it takes to reach a specified resource value (or skip after maximum allotted time)

    Initial values will be reported on the command line, if toggled, but full values will be reported in a csv file.

    """

    # Final output variables and building block generations
    final_list = []
    # Building block for helping generation build orders
    generate_orders_building_blocks = GenerateOrdersBuildingBlocks()

    print("Beginning execution...")
    # Main execution loop
    x = 0
    while x < NUMBER_OF_SIMULATION_LOOPS:
        # Instantiate SimulationWrapper object, which will take care of all the individual objects and variables needed
        # to run the simulation
        sim_wrapper = SimulatorWrapper(starting_money=STARTING_RESOURCES,
                                       debug_mode=DEBUG_MODE,
                                       fine_debug=FINE_DEBUG)

        # Add the number of bases desired. First base is different from others
        j = 0
        while j < NUMBER_OF_BASES:
            # first base starts off as a KEEP, other ones are empty
            if j == 0:
                sim_wrapper.add_base(upgrade_level=BaseLevel.KEEP,
                                     base_number=j+1)

            else:
                sim_wrapper.add_base(upgrade_level=BaseLevel.EMPTY,
                                     base_number=j+1)
            j += 1

        # Generate random build order and the runtime building blocks to run the generated order
        generated_build_order = generate_orders_building_blocks.generate_random_build_orders(sim_wrapper.base_list)

        # Check if the orders have already been done by checking the saved hash set.
        if not generate_orders_building_blocks.is_build_order_seen(generated_build_order):

            # Run the actual simulation
            final_sim_time = sim_wrapper.run_simulation(build_order=generated_build_order,
                                                        resource_trigger=RESOURCE_TRIGGER_VALUE,
                                                        simulation_time_seconds=SIMULATION_TIME_SECONDS)

            build_orders = generate_orders_building_blocks.build_order_print(generated_build_order)

            # If it has been requested to ignore runs without temple, do so, otherwise default to save all runs
            if REMOVE_IF_NO_TEMPLE:
                if "TEMPLE" in build_orders:
                    final_list.append([final_sim_time, build_orders])
            else:
                final_list.append([final_sim_time, build_orders])

        else:
            if DEBUG_MODE:
                print("Already have done build order, skipping")

        x += 1

    # Final print out logic and reporting to csv file
    RuntimeBuildingBlocks.results_to_csv(final_list, "results/output.csv")
    RuntimeBuildingBlocks.report_quickest_run(final_list)


main()
