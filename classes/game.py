import random


class BColors:
    """ This class allows us to use colors inside terminal.

    Public Constants:
        :cvar HEADER (string): Color Code
        :cvar OK_BLUE (string): Code for coloring the text BLUE in the Terminal.
        :cvar OK_GREEN (string): Code for coloring the text GREEN in the Terminal.
        :cvar WARNING (string): Color Code
        :cvar FAIL (string): Code for coloring the text RED  in the Terminal.
        :cvar ENDC (string): Code for coloring the text BLACK in the Terminal.
        :cvar BOLD (string): Code for making the text BOLD in the Terminal.
        :cvar UNDERLINE (string): Code for UNDERLINING the text in the Terminal.
    """

    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    """ This class is used to define the basic info for different units present in the game. """

    def __init__(self, name, hp, mp, atk, df, magic, items):
        """ Creates an instance of Person.

        Parameters:
            name(str): Name of the unit.
            hp(int): Hit points.
            mp(int): Magic points.
            atk(int): Attack points.
            df(int): Defense points.
            magic(list): A list of dictionaries with info about magic spells used by an unit; Each dictionary
                consist of three key-value pairs where each key is a string. They are:
                    "name": str
                    "cost": a non-negative int
                    "dmg": a non-negative int.
            items(list): A list of dictionaries with info about items used by an unit; Each dictionary consists of
                two key-values where each key is a string. They are:
                    "item": str
                    "quantity": a non-negative int.
        """
        self._name = name
        self._max_hp = hp
        self._hp = hp
        self._max_mp = mp
        self._mp = mp
        self._low_atk = atk - 10
        self._high_atk = atk + 10
        self._df = df
        self._magic = magic
        self._items = items
        # Actions available to the unit when its turn comes
        self._actions = ["Attack", "Magic", "Items"]

    def get_name(self):
        """ Returns the name of the unit. """
        return self._name

    def get_hp(self):
        """ Returns the remaining HP. """
        return self._hp

    def get_max_hp(self):
        """ Returns the maximum HP. """
        return self._max_hp

    def get_mp(self):
        """ Returns the remaining MP. """
        return self._mp

    def get_max_mp(self):
        """ Returns the maximum MP. """
        return self._max_mp

    def get_magic(self):
        """ Returns the list of spells that can be used by an unit. """
        return self._magic[:]

    def get_items(self):
        """ Returns the list of items that are present in the inventory of an unit. """
        return self._items[:]

    def set_hp_to_max(self):
        """ Set the HP of the unit to its maximum possible value. """
        self._hp = self._max_hp

    def set_mp_to_max(self):
        """ Set the MP of the unit to its maximum possible value. """
        self._mp = self._max_mp

    def reduce_mp(self, cost):
        """ Reduces the available MP depending on the cost of the spell being cast.

        Parameters:
            cost(int): Cost of the magic spell being cast.
        """
        self._mp -= cost

    def generate_damage(self):
        """ Randomly generates the amount of damage dealt by a physical attack on the target.

        :returns int: dmg dealt to the target.
        """
        return random.randint(self._low_atk, self._high_atk)

    def take_damage(self, dmg):
        """ Calculates the HP after damage was received by an unit.

        Parameters:
            dmg(int): Damage taken by the unit where dmg > 0.

        :returns int: HP of the unit after receiving damage.
        """
        self._hp -= dmg
        if self._hp < 0:
            self._hp = 0
        return self._hp

    def heal(self, dmg):
        """ Calculates the HP after a healing spell was cast.

        Parameters:
            dmg(int): Amount of HP restored where dmg > 0.

        :returns int: HP after being healed.
        """
        self._hp += dmg
        if self._hp > self._max_hp:
            self._hp = self._max_hp
        return self._hp

    def choose_action(self):
        """ Do the action specified by the player. """
        i = 1
        print("\n" + "    " + BColors.BOLD + self._name + BColors.ENDC)
        print(BColors.OK_BLUE + BColors.BOLD + "    ACTIONS:" + BColors.ENDC)
        for item in self._actions:
            print("        " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        """ Cast the spell specified by the player. """
        i = 1
        print("\n" + BColors.OK_BLUE + BColors.BOLD + "    MAGIC:" + BColors.ENDC)
        for spell in self._magic:
            print("        " + str(i) + ".", spell.get_name(), "(cost:", str(spell.get_cost()) + ")")
            i += 1

    def choose_enemy_spell(self):
        """ Return the name and the damage of the spell to be casted by an enemy.

        Randomly select a spell from the list of spells associated with an enemy and then, if the cost of spell
        allows the enemy to cast it, then, return the name and the damage generated by the randomly chosen spell;
        Otherwise, select another spell from the list which can be cast in the given MP.

        Returns a tuple with two elements, spell and a positive integer, magic damage.

        If no spell can be cast, return None and 0 to signify the same.
        """
        magic_choice = random.randrange(0, len(self._magic))
        spell = self._magic[magic_choice]
        magic_dmg = spell.generate_damage()

        health_pct = (self._hp / self._max_hp) * 100

        if self._mp < spell.get_cost() or health_pct > 50 and spell.get_type() == "white":
            self.choose_enemy_spell()

        return spell, magic_dmg

    def choose_item(self):
        """ Select the item to be used by the player. """
        i = 1
        print("\n" + BColors.OK_GREEN + BColors.BOLD + "    ITEMS:" + BColors.ENDC)
        for item in self._items:
            print("        " + str(i) + ".", item["item"].get_name() + ":", item["item"].get_description(), "(x"
                  + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        """ Select and return the index of the enemy that the player wish to target.

        :param list enemies: A list of possible targets for the player. All the element in the list should be an
                        instance of Person.

        Returns index of the targeted enemy where 0 <= index < len(enemies).
        """
        i = 1
        print("\n" + BColors.FAIL + BColors.BOLD + "    TARGET:" + BColors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.get_name())
                i += 1
        choice = int(input("    Choose target: ")) - 1
        return choice

    def get_stats(self):
        """ Display the stats of a player. """
        # Creating the Progress Bar to be displayed for HP
        hp_bar = ""
        bar_ticks = ((self._hp / self._max_hp) * 100) / 4
        # Filling a portion of the progress bar with █ to represent remaining HP depending upon the value of bar_ticks
        while bar_ticks > 0:
            hp_bar += '█'  # Code for ASCII character █ (called 'Block') is 219.
            bar_ticks -= 1
        # Using spaces ' ' to represent HP lost in the progress bar
        while len(hp_bar) < 25:
            hp_bar += " "

        # Creating the Progress Bar to be displayed for MP
        mp_bar = ""
        mp_ticks = ((self._mp / self._max_mp) * 100) / 10
        # Filling a portion of the progress bar with █ to represent remaining MP depending upon the value of bar_ticks
        while mp_ticks > 0:
            mp_bar += "█"  # Code for ASCII character █ (called 'Block') is 219.
            mp_ticks -= 1
        # Using spaces ' ' to represent MP lost in the progress bar
        while len(mp_bar) < 10:
            mp_bar += " "

        # Preventing text alignment from getting disturbed by dealing with whitespaces when HP drops a rightmost decimal
        hp_string = str(self._hp) + "/" + str(self._max_hp)
        current_hp = ""
        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string

        # Preventing text alignment from getting disturbed by dealing with whitespaces when MP drops a rightmost decimal
        mp_string = str(self._mp) + "/" + str(self._max_mp)
        current_mp = ""
        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)
            while decreased > 0:
                current_mp += " "
                decreased -= 1
            current_mp += mp_string
        else:
            current_mp = mp_string

        # Display player stats
        print("                      _________________________                 __________")
        print(BColors.BOLD + self._name + ":" + "    " + current_hp + " |"
              + BColors.OK_GREEN + hp_bar + BColors.ENDC + "|       " + BColors.BOLD
              + current_mp + " |" + BColors.OK_BLUE + mp_bar + BColors.ENDC + "|")

    def get_enemy_stats(self):
        """ Display stats of enemies. """
        # Creating the Progress Bar to be displayed for HP
        hp_bar = ""
        bar_ticks = ((self._hp / self._max_hp) * 100) / 2
        # Filling a portion of the progress bar with █ to represent remaining HP depending upon the value of bar_ticks
        while bar_ticks > 0:
            hp_bar += "█"  # Code for ASCII character █ (called 'Block') is 219.
            bar_ticks -= 1
        # Using spaces ' ' to represent HP lost in the progress bar
        while len(hp_bar) < 50:
            hp_bar += " "

        # Preventing text alignment from getting disturbed by dealing with whitespaces when HP drops a rightmost decimal
        hp_string = str(self._hp) + "/" + str(self._max_hp)
        current_hp = ""
        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string

        # Display player stats
        print("                      __________________________________________________")
        print(BColors.BOLD + self._name + ":" + "  " + current_hp + " |"
              + BColors.FAIL + hp_bar + BColors.ENDC + "|")

