import random


class Spell:
    """ This class handles all the data and the actions associated with magic spells.  """

    def __init__(self, name, cost, dmg, type_):
        """ Creates an instance of Spell.

        Parameters:
            name(str): Name of the Spell.
            cost(int): The MP cost associated with casting the Spell where cost is a positive integer.
            dmg(int): The amount of damage done by the Spell where dmg is a positive integer.
            type_(str): Type of Spell being cast. There are only two valid types:
                1. "black": This type of Spells do damage to the target.
                2. "white": This type of Spells heals the one casting it.
        """
        self._name = name
        self._cost = cost
        self._dmg = dmg
        self._type = type_

    def generate_damage(self):
        """ Randomly generates the amount of damage dealt by a specified spell on the target.

        :returns int: damage dealt to the target.
        """
        low_dmg = self._dmg - 15
        high_dmg = self._dmg + 15
        return random.randint(low_dmg, high_dmg)

    def get_name(self):
        """ Returns the name of the Spell. """
        return self._name

    def get_cost(self):
        """ Returns the MP cost associated with the Spell. """
        return self._cost

    def get_type(self):
        """ Returns the type of Spell being cast. """
        return self._type
