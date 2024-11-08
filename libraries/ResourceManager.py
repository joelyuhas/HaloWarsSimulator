"""
Halo Wars Simulator
March 25th, 2024

Resource Manger used for keeping track of the resources and tech levels in a specific game.

"""
import math


class ResourceManager:
    """
    Class to manage the resource accrual rate and tech levels. This is done by checking how many total supply pads and
    heavy supply pads there are, as well as providing methods to add and remove supply pads and tech levels.

    Args:
        building_supply_pad (int): Toggle if a supply pad is being built. Used by other programs for checking if
            resources will be coming or if a build skip is needed.
        supply_pad_lite_quantity (int): Total number of lite supply pads
        supply_pad_heavy_quantity (int): Total number of heavy supply pads
        current_money (int): Current amount of money available to the player
        current_tech_level (int):  Current tech level
        current_temple_count (int):  Current temple count. Can only be one temple.
    
    """
    def __init__(self):
        self.building_supply_pad = 0
        self.supply_pad_lite_quantity = 0
        self.supply_pad_heavy_quantity = 0
        self.current_money = 0
        self.current_tech_level = 0
        self.current_temple_count = 0

    def note_supply_pad_is_being_built(self):
        """
        Helper method that sets the building supply pad variable to 1. This notes that a supply pad is being built

        """
        self.building_supply_pad = 1

    def is_supply_pad_built_or_being_built(self) -> bool:
        """
        checks and returns if a supply pad is currently being built, or if one exist. Used by other programs to see if
        supplies will eventually be on their way or not.

        :return: Bool: true if a supply pad is built or being built. False if otherwise
        """
        if self.building_supply_pad > 0:
            return True
        else:
            return False

    def add_money(self, amount: int):
        """
        Add money to the resource manager. Primarily used for setting the starting amount of money, but can also be
        used for when teammates donate money.

        :param amount: int: The amount of money to add to the player.
        """
        self.current_money = self.current_money + amount

    def add_tech_level(self):
        """
        Increase the tech level.

        """
        self.current_tech_level = self.current_tech_level + 1

    def subtract_money(self, amount: int) -> bool:
        """
        Remove money from the total pool. Used primarily for buildings or units are purchased. If there is enough money,
        perform the subtraction and return True. Otherwise, return False.

        :param amount: int: The amount of money to subtract
        :return: bool: True if enough money and the subtraction has bene made. False if the subtraction cannot be made
        """
        if self.current_money >= amount:
            self.current_money = self.current_money - amount
            return True
        else:
            return False

    def add_temple(self):
        """
        Add a temple count. Note this is different from tech leve, as a temple can be being built, but a temple doesnt
        add a tech level until it's done.

        """
        self.current_temple_count = self.current_temple_count + 1

    def update(self) -> str:
        """
        Main update method. This method performs the calculation to see how many new resources are added to the money
        pool based on how many lite and heavy supply pads there are. This calculation is intended to take place for
        every in game second.

        Supply pad equation:
            - S is supply pad rate:
                - lite supply pads S = 2.5
                - heavy supply pads  S= 3.5
            - N is total number of suppy pads (lite + heavy)

            Supplies a second = (S * 1.75) / (((N / (9)) + 1) * N

            Equation is done twice, once for lite supply pads, another for heavy, then added together for total.

        Note: The "original" equation found online was (S * 1.5) / (((N / (13)) + 1) * N but it was found that this did
            not match in game supply rates. This was updated with trial and error and the current equation seems to be
            very accurate even over very long periods of in game time.

        :return: str: A string containing the calculation information, number of supply pads, types, and resources made
        """
        total_supply_pad = self.supply_pad_lite_quantity + self.supply_pad_heavy_quantity
        # Multiply by 10 and divide by 10 to round to the nearest decimal place. Also floor results.
        heavy_rate = math.floor(self.supply_pad_heavy_quantity * (3.5 * 1.75)/((total_supply_pad/9) + 1) * 10) / 10
        lite_rate = math.floor(self.supply_pad_lite_quantity * (2.5 * 1.75)/((total_supply_pad/9) + 1) * 10) / 10
        final_rate = math.floor((heavy_rate + lite_rate) * 10) / 10
        self.current_money = int(self.current_money + final_rate)
        return f"MONEY: {self.current_money} total: {final_rate} heavy: {heavy_rate} lite: {lite_rate}, lite Q: " \
               f"{self.supply_pad_lite_quantity} heavy Q {self.supply_pad_heavy_quantity}"

    def add_lite_supply_pad(self):
        """
        Helper method to add a lite supply pad to the resource manager.

        """
        self.supply_pad_lite_quantity = self.supply_pad_lite_quantity + 1

    def remove_lite_supply_pad(self):
        """
        Helper method to remove a lite supply pad to the resource manager.

        """
        self.supply_pad_lite_quantity = self.supply_pad_lite_quantity - 1

    def add_heavy_supply_pad(self):
        """
        Helper method to add a heavy supply pad to the resource manager.

        """
        self.supply_pad_heavy_quantity = self.supply_pad_heavy_quantity + 1

    def remove_heavy_supply_pad(self):
        """
        Helper method to remove a heavy supply pad to the resource manager.

        """
        self.supply_pad_heavy_quantity = self.supply_pad_heavy_quantity - 1