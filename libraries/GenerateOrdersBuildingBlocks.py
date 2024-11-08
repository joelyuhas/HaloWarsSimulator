"""
Halo Wars Simulator
March 19th, 2024

Building Blocks class file responsible for generating random build orders and utilities surrounding that

"""
import random

from libraries.BaseClass import Base
from libraries.BaseConstants import BaseLevel, BaseState, Orders, get_slot_number


class BaseBuildCounters:
    """
    Class used for keeping track of relative build slots available for each base when making the build orders. Note,
    this information is different from the info stored directly in the Base class since here build orders are being
    made, and the in order to see if they are valid, these checks are done before the bases are actually established
    and simulated.

    This helps prune out alot of invalid build orders.

    Args:
        base (Base): The reference base, which primarily is used to pass on to other areas in the code
        current_base_level (BaseLevel): The current base level, mostly in reference to the build orders that have been
            created, and not the actual, running base.

    """
    def __init__(self, base: Base, current_base_level=BaseLevel.EMPTY):
        self.base = base
        self.build_index = 1
        self.upgrade_supply_pad_index = 1
        self.current_base_level = current_base_level
        if current_base_level == BaseLevel.EMPTY:
            self.current_base_slots = 0
        elif current_base_level == BaseLevel.OUTPOST:
            self.current_base_slots = 3
        elif current_base_level == BaseLevel.KEEP:
            self.current_base_slots = 5
        elif current_base_level == BaseLevel.CITADEL:
            self.current_base_slots = 7
        self.base_status = BaseState.IDLE

    def increment_build_index(self):
        """
        Quick helper class to increment the build index.

        """
        self.build_index += 1

    def increment_upgrade_supply_pad_index(self):
        """
        Quick helper class to increment the upgraded supply pad index.

        """
        self.upgrade_supply_pad_index += 1

    def upgrade_base_level(self) -> bool:
        """
        Used to upgrade the theoretical base leve. So when a build order issues an UPGRADE_BASE command,then the build
        order program wil know that more build slots will be available after.

        :return: bool: return True if able to upgrade, False if not
        """
        if self.current_base_level == BaseLevel.EMPTY:
            self.current_base_level = BaseLevel.OUTPOST
            self.current_base_slots = 3
            return True
        if self.current_base_level == BaseLevel.OUTPOST:
            self.current_base_level = BaseLevel.KEEP
            self.current_base_slots = 5
            return True
        elif self.current_base_level == BaseLevel.KEEP:
            self.current_base_level = BaseLevel.CITADEL
            self.current_base_slots = 7
            return True
        else:
            return False


class GenerateOrdersBuildingBlocks:
    """
    The GenerateOrdersBuildingBlocks class is responsible for generating random build orders, ensuring they are valid,
    saving them appropriately, and skipping any builds that have already been done before by comparing their hashes.

    Class that creates an object that will generate random build orders with certain attributes. These attributes can
    be modified if needed so that multiple random build orders can be established/generated.

    Figured this could also just be a method, but by putting it in a class the values could be changed easily during an
    execution if needed.


    Args:
        build_supply_pad_range_lower (int): The lower value for which a supply pad build command will be generated
        build_supply_pad_range_upper (int): The upper value for which a supply pad build command will be generated
        build_temple_range_lower (int): The lower value for which a temple build command will be generated
        build_temple_range_upper (int): The upper value for which a temple build command will be generated
        upgrade_base_range_lower (int): The lower value for which a base upgrade build command will be generated
        upgrade_base_range_upper (int): The upper value for which a base upgrade build command will be generated
        upgrade_supply_pad_range_lower (int): The lower value for which a temple build command will be generated
        top_random_number_value (int): The max value for the random number for the build order select will be
        max_number_of_builds_in_build_order_random_top (int): Max value for how many orders to put in build order
        seen_hash_list (set): The set containing previously seen hash values used for comparison. This is a set
            for faster comparison compared to a list

    """
    def __init__(self,
                 build_supply_pad_range_lower=0,
                 build_supply_pad_range_upper=2,
                 build_temple_range_lower=2,
                 build_temple_range_upper=3,
                 upgrade_base_range_lower=3,
                 upgrade_base_range_upper=4,
                 upgrade_supply_pad_range_lower=4,
                 top_random_number_value=6,
                 max_number_of_builds_in_build_order_random_top=28):

        self.build_supply_pad_range_lower = build_supply_pad_range_lower
        self.build_supply_pad_range_upper = build_supply_pad_range_upper
        self.build_temple_range_lower = build_temple_range_lower
        self.build_temple_range_upper = build_temple_range_upper
        self.upgrade_base_range_lower = upgrade_base_range_lower
        self.upgrade_base_range_upper = upgrade_base_range_upper
        self.upgrade_supply_pad_range_lower = upgrade_supply_pad_range_lower
        self.top_random_number_value = top_random_number_value
        self.max_number_of_builds_in_build_order_random_top = max_number_of_builds_in_build_order_random_top
        self.seen_hash_list = set()

    def generate_random_build_orders(self, input_base_list: list[Base]) -> list:
        """
        Method that will generate random build orders given a list of bases. It will generate these random orders based
        on how many bases are in the list as well. So if one base in the list, orders will be generated for only one
        base. If multiple bases are in the list, that will be taken into effect.

        :param input_base_list: list[Base]: Input list with all bases that will be used
        :return: list: The build order list that has been generated

        """
        build_order = []

        # Be able to take in a dynamic amount of bases
        base_helper_list = []
        number_of_bases = len(input_base_list)-1
        i = 0
        for base in input_base_list:
            # If this is the first base, it starts as a KEEP. Any subsequent base starts as empty
            if i == 0:
                base_helper_list.append(BaseBuildCounters(base=base, current_base_level=BaseLevel.KEEP))
            else:
                base_helper_list.append(BaseBuildCounters(base=base, current_base_level=BaseLevel.EMPTY))
            i += 1

        random_build_order_length = random.randint(2, self.max_number_of_builds_in_build_order_random_top)
        # used to increment through the orders
        build_order_increment = 0

        # flags for checking the temples
        temple_build_flag_and_index = 0
        temple_build_base_number = 0

        # print("generating random build orders")

        while build_order_increment <= random_build_order_length:
            # random number to select base build
            r_b_s = random.randint(0, number_of_bases)
            # random number to select build order
            random_number = random.randint(0, self.top_random_number_value)

            # Build supply pad orders
            if self.build_supply_pad_range_lower <= random_number < self.build_supply_pad_range_upper:
                # Can only build x number of plots, upgrades when base is upgraded  slots in total
                if base_helper_list[r_b_s].build_index <= base_helper_list[r_b_s].current_base_slots:
                    build_order.append([Orders.BUILD_SUPPLY_PAD,
                                        base_helper_list[r_b_s].base,
                                        get_slot_number(base_helper_list[r_b_s].build_index)])
                    base_helper_list[r_b_s].increment_build_index()
                build_order_increment += 1

            # Build temple orders
            elif self.build_temple_range_lower <= random_number < self.build_temple_range_upper:
                if temple_build_flag_and_index == 0:
                    if base_helper_list[r_b_s].build_index <= base_helper_list[r_b_s].current_base_slots:
                        build_order.append([Orders.BUILD_TEMPLE,
                                            base_helper_list[r_b_s].base,
                                            get_slot_number(base_helper_list[r_b_s].build_index)])
                        # set the build flag to the index
                        temple_build_flag_and_index = base_helper_list[r_b_s].build_index
                        temple_build_base_number = r_b_s
                        base_helper_list[r_b_s].increment_build_index()
                        build_order_increment += 1

            # Upgrade base orders
            elif self.upgrade_base_range_lower <= random_number < self.upgrade_base_range_upper:
                # if the base level is properly upgraded, then increment
                if base_helper_list[r_b_s].upgrade_base_level():
                    build_order.append(
                        [Orders.UPGRADE_BASE, base_helper_list[r_b_s].base, None])
                    build_order_increment += 1

            # Upgrade supply pad orders
            elif random_number >= self.upgrade_supply_pad_range_lower:
                # ensure temple has been created
                if temple_build_flag_and_index > 0:
                    # ensure index is not out of range, which can happen if temple is made
                    if base_helper_list[r_b_s].build_index < 8:
                        # Ensure more supply pads than upgraded supply pads
                        if base_helper_list[r_b_s].upgrade_supply_pad_index < base_helper_list[r_b_s].build_index:
                            # Need to check which slot the temple is on and skip if needed
                            if temple_build_flag_and_index == base_helper_list[r_b_s].upgrade_supply_pad_index:
                                # check if on same base as the temple
                                if temple_build_base_number == r_b_s:
                                    # if in here, have selected the index and base of the temple, so skip
                                    base_helper_list[r_b_s].increment_upgrade_supply_pad_index()
                            else:
                                # if over here, have selected a supply pad, can upgrade
                                build_order.append([Orders.UPGRADE_SUPPLY_PAD,
                                                    base_helper_list[r_b_s].base,
                                                    get_slot_number(base_helper_list[r_b_s].upgrade_supply_pad_index)])
                                base_helper_list[r_b_s].increment_upgrade_supply_pad_index()
                                build_order_increment += 1
        return build_order

    def get_build_order_hash(self, build_order: list) -> hash:
        """
        Generate a hash of the build order list so it can be cross compared later on. Perform the print operation on
        the build order list as well, so it can be hashed correctly (otherwise the object addresses print out which
        changes the hash values)

        :param build_order: List: The build order in its list format.
        :return: hash: The value of the hash that was performed on the build order.

        """
        return hash(self.build_order_print(build_order))

    def is_build_order_seen(self, build_order: list) -> bool:
        """
        Take in a build order list. Print the build order using the build_order_print helper method, and check a given
        hash list to see if it has been seen before. If it has, add it to the list.

        This way, all the needed checks, conversions, and additions happen inside this method for simplicity. Decided
        to NOT include the seen_hash_list in the class itself in case the clas sis re-used, and there are values still
        populated within it.

        :param build_order: List: The build order in its list format.
        :return: bool: True if the build order has been seen in the previous hash list, false if not

        """
        build_order_hash = self.get_build_order_hash(build_order)
        if build_order_hash in self.seen_hash_list:
            return True
        else:
            self.seen_hash_list.add(build_order_hash)
            return False

    @staticmethod
    def build_order_print(build_order: list) -> str:
        """
        Take a build order, which is normally composed of a list of lists, (build type, base object, build slot) and
        convert to a string. This string is the build order in chronological order, with the build order name shortened
        to be more readable, as well as the base number it is built on.

        :param build_order: List: The build order in its list format.
        :return: str: The build order sting that has been correctly formatted

        """
        build_string = ""

        for order in build_order:
            if str(order[0]) == "Orders.BUILD_SUPPLY_PAD":
                build_string = build_string + "SUPPLY " + str(order[1].base_number) + ", "
            elif str(order[0]) == "Orders.UPGRADE_SUPPLY_PAD":
                build_string = build_string + "U_SPLY " + str(order[1].base_number) + ", "
            elif str(order[0]) == "Orders.BUILD_TEMPLE":
                build_string = build_string + "TEMPLE " + str(order[1].base_number) + ", "
            elif str(order[0]) == "Orders.UPGRADE_BASE":
                build_string = build_string + "U_BASE " + str(order[1].base_number) + ", "
            elif str(order[0]) == "SKIPPED":
                # Note, previously had the skipped value print from here, but found it made reading the results
                # confusing
                pass
            else:
                build_string = str(order[0]) + ", "
        return build_string
