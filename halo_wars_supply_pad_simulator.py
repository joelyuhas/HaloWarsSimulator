"""
Halo Wars Simulator
March 19th, 2024

Prototyping executable. Used for testing and running specific, handcrafted, build orders

No random build orders, manual testing can be done.

Sandbox testing.

"""
from libraries.ResourceManager import ResourceManager
from libraries.BaseClass import Base
from libraries.BaseConstants import *
from libraries.RuntimeBuildingBlocks import RuntimeBuildingBlocks


debug_mode = True

# Instantiate all the needed objects and class packs
resource_manager = ResourceManager()
resource_manager.add_money(800)
first_base = Base(resource_manager=resource_manager,
                  upgrade_level=BaseLevel.KEEP,
                  print_mode=debug_mode,
                  base_number=1)
second_base = Base(resource_manager=resource_manager,
                   upgrade_level=BaseLevel.EMPTY,
                   print_mode=debug_mode,
                   base_number=2,
                   pause_timer=30,
                   temple_needed_to_clear_second_base=True)


# Overall build order test
build_orders = [
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_1],
    [Orders.BUILD_SUPPLY_PAD, second_base, SlotNumbers.build_slot_1],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_1],
    [Orders.BUILD_TEMPLE, first_base, SlotNumbers.build_slot_2],
    [Orders.BUILD_TEMPLE, first_base, SlotNumbers.build_slot_2],
    [Orders.UPGRADE_SUPPLY_PAD, first_base, SlotNumbers.build_slot_1],
    [Orders.UPGRADE_SUPPLY_PAD, first_base, SlotNumbers.build_slot_1],
    [Orders.UPGRADE_SUPPLY_PAD, first_base, SlotNumbers.build_slot_7],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_3],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_4],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_5],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_6],
    [Orders.UPGRADE_BASE, first_base, None],
    [Orders.UPGRADE_BASE, second_base, None],
    [Orders.BUILD_SUPPLY_PAD, second_base, SlotNumbers.build_slot_6],
    [Orders.BUILD_SUPPLY_PAD, second_base, SlotNumbers.build_slot_1],
    [Orders.BUILD_SUPPLY_PAD, second_base, SlotNumbers.build_slot_2],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_6],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_7],
]


# Test to ensure certain build orders will be skipped
build_orders_2 = [
    [Orders.BUILD_TEMPLE, first_base, SlotNumbers.build_slot_1],
    [Orders.UPGRADE_BASE, first_base, None],
    [Orders.UPGRADE_BASE, second_base, None],
    [Orders.UPGRADE_BASE, second_base, None],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_3],
]


build_orders_3 = [
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_1],
    [Orders.UPGRADE_BASE, second_base, None],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_2],
    [Orders.BUILD_SUPPLY_PAD, second_base, SlotNumbers.build_slot_1],
    [Orders.BUILD_SUPPLY_PAD, second_base, SlotNumbers.build_slot_2],
    [Orders.BUILD_SUPPLY_PAD, second_base, SlotNumbers.build_slot_3],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_3],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_4],
    [Orders.BUILD_TEMPLE, first_base, SlotNumbers.build_slot_5],
    [Orders.UPGRADE_SUPPLY_PAD, second_base, SlotNumbers.build_slot_1],
    [Orders.UPGRADE_BASE, second_base, None],
    [Orders.UPGRADE_SUPPLY_PAD, first_base, SlotNumbers.build_slot_1],
    [Orders.UPGRADE_SUPPLY_PAD, first_base, SlotNumbers.build_slot_2],
    [Orders.UPGRADE_SUPPLY_PAD, first_base, SlotNumbers.build_slot_3],
    [Orders.UPGRADE_SUPPLY_PAD, second_base, SlotNumbers.build_slot_2],
    [Orders.UPGRADE_SUPPLY_PAD, second_base, SlotNumbers.build_slot_3],
]

# Test that the pause timer will function correctly
build_orders_4 = [
    [Orders.BUILD_TEMPLE, first_base, SlotNumbers.build_slot_1],
    [Orders.UPGRADE_BASE, second_base, None],
    [Orders.BUILD_SUPPLY_PAD, first_base, SlotNumbers.build_slot_3],
]

# Bare bones simulation run.
base_list = [first_base, second_base]
runtime_building_blocks = RuntimeBuildingBlocks(resource_manager=resource_manager, print_mode=debug_mode)
final_sim_time = runtime_building_blocks.run_simulation(build_orders=build_orders,
                                                        resource_amount=3000,
                                                        simulation_time_max=2000,
                                                        base_list=base_list)


