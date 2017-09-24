NOTE: To run the game, unzip all game files into a single directory, then run game.py.

I made this game alone. (Or, at least, I coded it alone; my testers, while they did nothing to directly alter the game's code, definitely contributed to the making of the game, and deserve to have that contribution acknowledged.)

List of improvements I've made: (Note that I didn't use the starter code, so my engine might differ somewhat from standard)

"drop" command (1 point, total 1):
    Added a command, "drop", which makes the player drop an item from their inventory. If they have more than one of the item they're trying to drop, they'll only drop one of them. Works by appending the item to their room's list of contents and then deleting it from their inventory's list of items-with-that-name.

"me" command (2 points, total 3):
    Added a command, "self" (also known as "me"), which prints the player character's name, health, carried gold, and known spells.

Bigger world (2 points, total 5):
    My rooms system allows for arbitrarily many rooms to be stitched together, with each room attaching to up to six others (one each to the north, south, east, west, up, and down). The world I've actually implemented in the game contains 25 rooms, each with at least two descriptions (one to be displayed on entry, one if the player examines it).

"inspect" command (2 points, total 7):
    Added a command, "examine" (also known as "look, "check", and "inspect"), which will display an object, creature, or room's description as long as it's in the same room as the player, in a container in the same room as the player, in the player's inventory, or is the room the player is standing in. Examining opened containers will display a list of their contents.

Weapons (2 points, total 9):
    Added a class, Weapon, which has a function associated with it, can be equipped, and when equipped will give the player a new option in combat to attack with that weapon (which will then run its associated function on the player's opponent). So, for instance, there's a knife, whose function does 10 damage to the target. None of the weapons I've implemented in the game do anything fancier than dealing damage, but such a weapon would be supported by the engine.

Victory condition (2 points, total 11):
    When the player either kills or nonlethally pacifies the game's final boss, Queen Melthar, they win and the game ends.

Healing items (2 points, total 13):
    Added a class, Potion, which can be consumed to apply a function to the player. Added a specific instance of that class, the "health potion" item, whose function heals the player, with its healing scaling negatively with the player's health (that is, the lower the player's health, the more the potion heals).

Locked chests (2 points, total 15):
    Added a class, LockedContainer, which inherits from the Container class (see below), but can't be opened unless the player has a specific key in their inventory (which will be consumed in the process of opening the container, to reduce clutter, and leave the container permanently unlocked)

Locked doors (2 points, total 17):
    Added a class, LockedDoor, which has a key system identical to the locked chests' (see above), but when opened will disappear and create a new exit to the room the player is in, leading in a defined direction to a defined destination room.

Containers (2 points, total 19):
    Added a class, Container, which consists of objects that store items identically to how the player's inventory stores items. When opened, items can be placed into and taken out of a container; when closed, neither of those things can be done.

Stacking items (2 points, total 21):
    The player's inventory consists of a dictionary of lists, with each list keyed to the name of the item they're carrying and containing all held items with that name. When the length of one of those lists is greater than 1, rather than individually listing out each item in the list, the "inventory" command will just list "Nx [itemname]", where N is equal to the length of the list.

More monsters (3 points, total 24):
    All NPCs the player interacts with are "monsters" in the sense that they can be fought; they each have different health values and attacks, and a couple of them have complex scripts to make fighting them most interesting (including one which turns into another creature upon death and one which randomly chooses between three attacks rather than always using the same one).

Special rooms (3 points, total 27):
    Added a class, SpecialRoom, which inherits from Room but has the extra input of a command, which is then run every time the player ends their turn in the room, and has flags which can track specific properties of the room. This system can be used both for basic effects like "heal on entry" (by healing the player and then setting an Entered flag to prevent them from healing further) and more complex effects like "roll for random encounter every time the player ends a turn here".

Command abbreviations (2 points*, total 29):
    Added a large number of aliases to commands. So, for instance, the "move" command can also be triggered by typing "go", or just the name of a direction without a preceding command (or, for that matter, the first letter of a direction without a preceding command); "examine" can also be triggered by typing "look", "check", or "inspect"; and so on for other commands, generally with as many useful aliases as I could think of.
    *I asked Adam about the point value of my implementation over email, and he told me this sounded like it was worth two points, so that's what I'm listing here.

Currency (4 points, total 33):
    Player has a count of gold carried, which can be used in interactions with a couple NPCs (one housing manager and one shopkeeper) to buy items from them (a key to a house in one case, the most powerful non-debug weapon in the game in the other case). Also, it can be given to a beggar, which has no particular gameplay benefit but makes the beggar happy.

Magic (3 points*, total 36):
    The player character knows two spells, each of which can be cast at any time to cause a particular effect in the world (healing characters in the case of the Heal spell, causing effects determined by the specific target in the case of the Flare spell).
    *I asked Adam about the point value of my implementation during a conversation, and he said it would probably be worth one less point given that the prompt asks for a restriction on casting frequency and my version has no such restriction, so I'm listing it as 3 points rather than 4.

Characters (4 points, total 40):
    There are lots of NPCs with varyingly-complex conversation trees, some of which only give you information, but many of which have gameplay effects of some sort (giving you items, for instance).

Interaction system (2 points*, total 42):
    Rather than keeping combat and conversation as separate gameplay systems, I put the two of them into a single system, wherein the player has options to talk, attack, cast spells at, or examine the NPC they're interacting with, as well as attempt to leave the interaction. The latter two run functions; the former three take the player into a subtree (the conversation subtree, the combat subtree, and the casting subtree) from which they then get a list of functions specific to the circumstance (the conversation subtree contains the NPC's dialogue options, the combat subtree contains the player's attacks, and the casting subtree contains the player's known spells).
    NPCs can be given overrides over specific parts of the interaction system, changing what a particular subtree looks like or what a particular command does within interactions with that NPC (for instance, some hostile NPCs prevent the "leave" command from working until they're killed).
    *I asked Adam about the point value of this over email, and he said it was worth two points.

In-depth help command (2 points*, total 44):
    In addition to "help" providing a list of commands, I have help submenus for each command in that list, accessible by typing "help [commandname]". These submenus list all of the command's aliases, what inputs it takes, and the details of what it does. A given submenu can be accessed by any alias of the command it describes; for instance, "help move" and "help go" will both list the same help page.
    *I asked Adam about the point value of this over email, and he said it was worth two points.