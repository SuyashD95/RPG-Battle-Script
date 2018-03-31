import random

from classes.game import BColors, Person
from classes.magic import Spell
from classes.inventory import Item
# Using colorama library to display colored text on Windows Command Prompt (cmd)
from colorama import init, deinit

# Display player stats
# init() will filter ANSI escape sequences out of any text sent to stdout or stderr, and replace them with
# equivalent Win32 calls
init()

# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
quake = Spell("Quake", 14, 140, "black")
meteor = Spell("Meteor", 40, 1200, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 35, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


# Create Some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
mega_elixir = Item("Mega Elixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Player Spells and Inventory
player_spells = [fire, thunder, blizzard, quake, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hi_potion, "quantity": 5},
                {"item": super_potion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": mega_elixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Enemy Spells and Inventory
enemy_spells = [fire, meteor, curaga]

# Instantiate People
player1 = Person(name="Valos ", hp=3260, mp=132, atk=300, df=34, magic=player_spells, items=player_items)
player2 = Person(name="Suyash", hp=4160, mp=188, atk=310, df=34, magic=player_spells, items=player_items)
player3 = Person(name="Alexis", hp=3090, mp=174, atk=290, df=34, magic=player_spells, items=player_items)

enemy1 = Person(name="Imp   ", hp=1250, mp=130, atk=560, df=325, magic=enemy_spells, items=[])
enemy2 = Person(name="Magnus", hp=18200, mp=700, atk=525, df=25, magic=enemy_spells, items=[])
enemy3 = Person(name="Imp   ", hp=1250, mp=130, atk=560, df=325, magic=enemy_spells, items=[])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

# Creating a flag to know the status of the while loop
running = True
# Styling the text that appears in the Terminal
print(BColors.FAIL + BColors.BOLD + "AN ENEMY ATTACKS!" + BColors.ENDC)

while running:
    print("======================")

    print("\n\n")
    print("NAME                  HP                                        MP")
    for player in players:
        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].get_name().replace(" ", "") + " for", dmg, "points of damage.")

            # Remove the killed enemy from the list of enemies.
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].get_name().replace(" ", "") + " has DIED.")
                del(enemies[enemy])
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            # Allow the player to move back to the top-menu if they press 0
            if magic_choice == -1:
                continue

            spell = player.get_magic()[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.get_cost() > current_mp:
                print(BColors.FAIL + "\nNot enough MP\n" + BColors.ENDC)
                continue

            player.reduce_mp(spell.get_cost())

            if spell.get_type() == "white":
                player.heal(magic_dmg)
                print(BColors.OK_BLUE + "\n" + spell.get_name() + " heals for " + str(magic_dmg), "HP." + BColors.ENDC)
            elif spell.get_type() == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(BColors.OK_BLUE + "\n" + spell.get_name() + " deals " + str(magic_dmg), "points of damage to "
                      + enemies[enemy].get_name().replace(" ", "") + "." + BColors.ENDC)

                # Remove the killed enemy from the list of enemies.
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].get_name().replace(" ", "") + " has DIED.")
                    del (enemies[enemy])
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            # Allow the player to move back to the top-menu if they press 0
            if item_choice == -1:
                continue

            item = player.get_items()[item_choice]["item"]

            if player.get_items()[item_choice]["quantity"] == 0:
                print(BColors.FAIL + "\n" + "None left..." + BColors.ENDC)
                continue

            player.get_items()[item_choice]["quantity"] -= 1

            if item.get_type() == "potion":
                player.heal(item.get_prop())
                print(BColors.OK_GREEN + "\n" + item.get_name() + " heals for", item.get_prop(), "HP." + BColors.ENDC)
            elif item.get_type() == "elixir":
                if item.get_name() == "Mega Elixir":
                    for member in players:
                        member.set_hp_to_max()
                        member.set_mp_to_max()
                    print(BColors.OK_GREEN + "\n" + item.get_name() +
                          " fully restores HP/MP of all the party members." + BColors.ENDC)
                else:
                    player.set_hp_to_max()
                    player.set_mp_to_max()
                    print(BColors.OK_GREEN + "\n" + item.get_name() + " fully restores HP/MP." + BColors.ENDC)
            elif item.get_type() == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.get_prop())
                print(BColors.FAIL + "\n" + item.get_name() + " deals", item.get_prop(), "points of damage to "
                      + enemies[enemy].get_name().replace(" ", "") + "." + BColors.ENDC)

                # Remove the killed enemy from the list of enemies.
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].get_name().replace(" ", "") + " has DIED.")
                    del (enemies[enemy])

    # Check if Player wins
    if len(enemies) == 0:
        print(BColors.OK_GREEN + "You WIN!" + BColors.ENDC)
        running = False
    # Check if Enemy wins
    elif len(players) == 0:
        print(BColors.FAIL + "Your enemies have DEFEATED you!" + BColors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randint(0, 2)

        if enemy_choice == 0:
            # Choose attack
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.get_name().replace(" ", "") + " attacks " + players[target].get_name().replace(" ", "")
                  + " for " + str(enemy_dmg), "points of damage.")

            # Remove the killed player from the list of players.
            if players[target].get_hp() == 0:
                print(players[target].get_name().replace(" ", "") + " has DIED.")
                del (players[target])
        elif enemy_choice == 1:
            (spell, magic_dmg) = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.get_cost())

            if spell.get_type() == "white":
                enemy.heal(magic_dmg)
                print(BColors.OK_BLUE + "\n" + spell.get_name() + " heals " + enemy.get_name().replace(" ", "") + " for "
                      + str(magic_dmg), "HP." + BColors.ENDC)
            elif spell.get_type() == "black":
                target = random.randint(0, 2)
                players[target].take_damage(magic_dmg)
                print(BColors.OK_BLUE + "\n" + enemy.get_name().replace(" ", "") + "'s " + spell.get_name() + " deals "
                      + str(magic_dmg), "points of damage to " + players[target].get_name().replace(" ", "") + "."
                      + BColors.ENDC)

                # Remove the killed player from the list of players.
                if players[target].get_hp() == 0:
                    print(players[target].get_name().replace(" ", "") + " has DIED.")
                    del (players[target])

# To stop using colorama before your program exits, simply call deinit(). This will restore stdout and stderr to
# their original values, so that Colorama is disabled.
deinit()
