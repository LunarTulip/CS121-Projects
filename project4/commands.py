#This module contains the text parser, a few helper functions, and all the commands the player can input

import scripts
import engine
import interactions

##############
#   Engine   #
##############

enabledcommands0 = []
enabledcommands1 = []

def checkdeath():
    if scripts.currprotag.dead:
        input("\nYou are dead. When you are ready to exit the game, press ENTER.")
        scripts.running = False
    elif scripts.currprotag.won:
        input('\nYou win. When you are ready to exit the game, press ENTER.')
        scripts.running = False

def parser():
    scripts.running = True #Debug line; necessary for the 'exitparser' command to work at full potential
    while scripts.running:
        inpt = input('\n>').lower()
        spaceindex = None
        if ' ' in inpt:
            spaceindex = inpt.index(' ')
        if spaceindex == None:
            if inpt in enabledcommands0:
                exec(inpt+'()')
            elif inpt in enabledcommands1:
                subject = input('What would you like to '+inpt+'?\n>').lower() #Customize phrasing per command
                exec(inpt+'("'+subject+'")')
            else:
                print("'"+inpt+"'"+' is not a recognized command. If you are stuck, type "help" to see a list of available commands.')
        else:
            command = inpt[:spaceindex]
            subject = inpt[spaceindex + 1:]
            if command in enabledcommands1:
                exec(command+'("'+subject+'")')
            elif command in enabledcommands0:
                exec(command+'()')
            else:
                print("'"+command+"'"+' is not a recognized command. If you are stuck, type "help" to see a list of available commands.')
        if hasattr(scripts.currprotag.location, 'loop'):
            exec(scripts.currprotag.location.loop)
        checkdeath()

def parser2(st, connectors, verb):
    part1 = None
    part2 = None
    for item in connectors:
        if " "+item+" " in st:
            part1 = st[:st.index(' '+item+' ')]
            part2 = st[st.index(' '+item+' ') + len(item) + 2:]
            break
    if not part1:
        for item in connectors:
            if " "+item in st:
                part1 = st[:st.index(' '+item)]
                part2 = input("What would you like to "+verb+" "+st+"?\n>").lower() #Customize phrasing per command
        if not part1:
            part1 = st
            part2 = input("What would you like to "+verb+" "+st+" "+connectors[0]+"?\n>").lower()
    return [part1, part2]

#################################
#   Help and related commands   #
#################################

helpdb = {}

def help(topic = None):
    if topic == None:
        print("List of commands:\n'help': Tells you the details of what a command does.\n'move': Moves you in a particular direction.\n'look': Examines an object or character.\n'get': Picks up an item from the ground or a container.\n'drop': Drops an item.\n'open': Opens a container.\n'unlock': Unlocks a locked container or door.\n'close': Closes a container.\n'put': Places an item inside a container.\n'drink': Drinks a potion.\n'equip': Equips a weapon.\n'me': Shows your stats and known spells.\n'inventory': Shows what you're holding.\n'interact: Starts an interaction with an NPC.\n'cast': Casts a spell.\n\nFor further information on any particular command, type 'help [command name]' (for instance, for more information on the 'help' command, you would type 'help help'). This information includes its aliases and abbreviations, what inputs it accepts, and a detailed description of its functionality.")
    elif topic in helpdb:
        print(helpdb[topic])
    else:
        helphelp = input("'"+topic+"' has no associated help page. Would you like to see the 'help' command's help page? Y/N\n>").lower()
        if helphelp == 'y' or helphelp == 'yes':
            help('help')
h = help

enabledcommands0 += ["help", "h"]
enabledcommands1 += ["help", "h"]
helpdb = {**helpdb, **dict.fromkeys(['help', 'h'], "Command aliases: 'help', 'h'\nValid inputs: Names of other commands or of spells (optional)\nDescription: If run without an input, gives a list of available commands. If run with an input, explains the function of the input command or spell.")}

#################################
#   Move and related commands   #
#################################

def move(direction):
    print(scripts.currprotag.move(direction))
go = move

def north():
    move('north')
n = north

def south():
    move('south')
s = south

def east():
    move('east')
e = east

def west():
    move('west')
w = west

def up():
    move('up')
u = up

def down():
    move('down')
d = down

enabledcommands0 += ["north", "south", "east", "west", "up", "down", "n", "s", "e", "w", "u", "d"]
enabledcommands1 += ["move", "go"]
helpdb = {**helpdb, **dict.fromkeys(['move', 'go', 'north', 'south', 'east', 'west', 'up', 'down', 'n', 's', 'e', 'w', 'u', 'd'], "Command aliases: 'move', 'go', [direction], [first letter of direction]\nValid inputs: Directions (north, south, east, west, up, down)\nDescription: Your character attempts to move in the input direction. Can also be run by typing the name of a direction, even without 'move' or 'go' preceding it.")}

####################################
#   Examine and related commands   #
####################################

def examine(subject = None):
    if subject == None or subject == 'room':
        print(scripts.currprotag.location.description)
        for item in scripts.currprotag.location.contents:
            if hasattr(item, 'shortdesc'):
                print(item.shortdesc+" ("+item.name+")")
        activeexits = []
        for direction in scripts.currprotag.location.exits:
            if scripts.currprotag.location.exits[direction]:
                activeexits.append(direction)
        if len(activeexits) >= 1:
            print("\nYou see exits in the following directions:")
            for item in activeexits[:-1]:
                print(item[0].upper()+item[1:]+", ", end='')
            print(activeexits[-1][0].upper()+activeexits[-1][1:]+".")
    else:
        if subject in scripts.currprotag.inventory:
            print(scripts.currprotag.inventory[subject][0].description)
            return None
        for item in scripts.currprotag.location.contents:
            if hasattr(item, 'description') and item.name.lower() == subject:
                result = item.description
                if isinstance(item, engine.Container):
                    if item.opened == False:
                        result += " It is closed."
                    elif len(item.contents) == 0:
                        result += " It is empty."
                    else: #len(item.contents) > 0
                        result += "\n\nIt contains the following items:"
                        for thing in item.contents:
                            if len(item.contents[thing]) == 1:
                                result += "\n"+item.contents[thing][0].name
                            else: #len(item.contents[thing]) > 1
                                result += "\n"+str(len(item.contents[thing]))+"x "+item.contents[thing][0].name
                print(result)
                return None
        for object in scripts.currprotag.location.contents:
            if isinstance(object, engine.Container) and object.opened == True:
                for item in object.contents:
                    if item == subject and hasattr(object.contents[item][0], 'description'):
                        print(object.contents[item][0].description)
                        return None
        print("You don't see any '"+subject+"' around.")
look = examine
check = examine
inspect = examine
l = examine

enabledcommands0 += ["examine", "look", "check", "inspect", 'l']
enabledcommands1 += ["examine", "look", "check", "inspect", 'l']
helpdb = {**helpdb, **dict.fromkeys(['examine', 'look', 'check', 'inspect', 'l'], "Command aliases: 'examine', 'look', 'check', 'inspect', 'l'\nValid inputs: Items or creatures in the same room as you (optional)\nDescription: If run without an input, describes the room you're standing in. If run with an input, describes the input item or creature.")}

###################################
#   Pickup and related commands   #
###################################

def pickup(item):
    result = scripts.currprotag.pickup(item)
    if "Could not find" in result:
        for object in scripts.currprotag.location.contents:
            if hasattr(object, 'opened') and object.opened and item in object.contents:
                print(scripts.currprotag.withdraw(item, object.name.lower()))
                return None
    print(result)
get = pickup
take = pickup
g = pickup

def drop(item):
    droppedweap = False
    if scripts.currprotag.inventory[item][0] == scripts.currprotag.weapon1:
        droppedweap = scripts.currprotag.weapon1.name
        scripts.currprotag.weapon1 = None
        scripts.currprotag.fighttree.remove(3)
    elif scripts.currprotag.inventory[item][0] == scripts.currprotag.weapon2:
        droppedweap = scripts.currprotag.weapon2.name
        scripts.currprotag.weapon2 = None
        scripts.currprotag.fighttree.remove(4)
    print(scripts.currprotag.drop(item))
    if droppedweap:
        print('You are no longer using '+droppedweap+' as a weapon.')
putdown = drop

def open(container):
    result = scripts.currprotag.open(container)
    if " is locked" in result:
        unlockresult = scripts.currprotag.unlock(container)
        if "Unlocked " in unlockresult:
            result = scripts.currprotag.open(container)
            print(unlockresult)
            if not "Could not find " in result:
                print(result)
            return None
    print(result)
o = open

def unlock(lockedthing):
    print(scripts.currprotag.unlock(lockedthing))

def close(container):
    print(scripts.currprotag.close(container))

def put(item):
    subdivision = parser2(item, ['in', 'on'], 'put')
    print(scripts.currprotag.place(subdivision[0], subdivision[1]))
place = put

enabledcommands1 += ["pickup", "get", "take", "g", "drop", "open", "o", "unlock", "close", "put", "place"]
helpdb = {**helpdb, **dict.fromkeys(['pickup', 'get', 'take', 'g'], "Command aliases: 'pickup', 'get', 'take', 'g'\nValid inputs: Items in the same room as you or in containers in the same room as you\nDescription: Attempts to pick up the input item, moving it from the room or container to your inventory.")}
helpdb = {**helpdb, **dict.fromkeys(['drop', 'putdown'], "Command aliases: 'drop', 'putdown'\nValid inputs: Items in your inventory\nDescription: Attempts to drop the input item, moving it from your inventory to the room you're standing in.")}
helpdb = {**helpdb, **dict.fromkeys(['open', 'o'], "Command aliases: 'open', 'o'\nValid inputs: Closed containers or locked doors in the same room as you\nDescription: If a container is input, attempts to open the input container, allowing you to add and remove items from it. If the container is locked, attempts to unlock it (see 'unlock' command for details) before attempting to open. If a door is input, attempts to unlock the door.")}
helpdb['unlock'] = "Command aliases: 'unlock'\nValid inputs: Locked doors or containers in the same room as you\nDescription: Attempts to unlock the input object. If you have the correct key in your inventory, will succeed, allowing you to open the container or move through the door, and will consume the key in the process, removing it from your inventory. Otherwise will fail, leaving the object still locked."
helpdb['close'] = "Command aliases: 'close'\nValid inputs: Open containers in the same room as you\nDescription: Attempts to close the input container, preventing you from adding and removing items to and from it."
helpdb = {**helpdb, **dict.fromkeys(['put', 'place'], "Command aliases: 'put', 'place'\nValid inputs: Items in your inventory and opened containers in the same room as you (one each, connected by the words 'in' or 'on', e.g. "+'"place book on shelf"'+"\nDescription: Moves the input item from your inventory into the input container.")}

################################
#   Use and related commands   #
################################

def use(item):
    print(scripts.currprotag.use(item))
drink = use

def equip(weapon):
    print(scripts.currprotag.equip(weapon))
wield = equip

enabledcommands1 += ["use", "drink", "equip", "wield"]
helpdb = {**helpdb, **dict.fromkeys(['use', 'drink'], "Command aliases: 'use', 'drink'\nValid inputs: Potions in your inventory\nDescription: Consumes the input potion, applying its effects to you and removing it from your inventory.")}
helpdb = {**helpdb, **dict.fromkeys(['equip', 'wield'], "Command aliases: 'equip', 'wield'\nValid inputs: Weapons in your inventory\nDescription: Attempts to equip the input weapon, allowing you to use its associated attack in combat.")}

#################################
#   Self and related commands   #
#################################

def self():
    print(scripts.currprotag.description)
    print("You are currently carrying "+str(scripts.currprotag.gold)+" gold.")
    print("Your current health is "+str(scripts.currprotag.health)+".")
    print("You know the following spells: "+scripts.currprotag.spellnames[0]+", "+scripts.currprotag.spellnames[1])
me = self

def inventory():
    if len(scripts.currprotag.inventory) > 0:
        print("Your inventory contains:")
        for item in scripts.currprotag.inventory:
            if len(scripts.currprotag.inventory[item]) == 1:
                print(scripts.currprotag.inventory[item][0].name)
            else: #len(scripts.currprotag.inventory[item]) > 1
                print(str(len(scripts.currprotag.inventory[item]))+"x "+scripts.currprotag.inventory[item][0].name)
    else:
        print("Your inventory is empty.")
inv = inventory
i = inventory

enabledcommands0 += ["inventory", "inv", "i", "self", "me"]
helpdb = {**helpdb, **dict.fromkeys(['self', 'me'], "Command aliases: 'self', 'me'\nValid inputs: None\nDescription: Displays your description, your known spells, and your current amounts of money and health.")}
helpdb = {**helpdb, **dict.fromkeys(['inventory', 'inv', 'i'], "Command aliases: 'inventory', 'inv', 'i'\nValid inputs: None\nDescription: Lists all items currently in your inventory by name, as well as how many of each you are holding.")}

#####################################
#   Interact and related commands   #
#####################################

def interact(npcname, entrypoint = None, refreshatstart = False):
    for item in scripts.currprotag.location.contents:
        if item.type == 'character' and item.name.lower() == npcname and item != scripts.currprotag:
            interaction = engine.Interaction(scripts.currprotag, item, entrypoint)
            if interaction.npc.hostile:
                npcfriendliness = 'hostile'
            else:
                npcfriendliness = 'friendly'
            print("\nYou are now interacting with "+interaction.npc.name+". "+interaction.npc.pronoun+" looks "+npcfriendliness+".")
            if refreshatstart:
                interaction.checkloop()
            while interaction.running:
                print("\nYou have the following options:")
                for i in range(len(interaction.curr.descriptions)):
                    print(str(i+1)+': '+interaction.curr.descriptions[i+1])
                choice = input('\n>')
                while not (choice.isdigit() and int(choice) in interaction.curr.contents):
                    print('Please input one of the listed numbers.')
                    choice = input('\n>')
                interaction.interact(int(choice))
            print("\nYou are no longer interacting with "+item.name+".")
            return None
        elif item.type != 'character' and item.name.lower() == npcname:
            print("You cannot interact with "+item.name+".")
            return None
    print("You don't see any '"+npcname+"' around.")

def talk(npc):
    interact(npc, 1)
speak = talk
chat = talk
t = talk

def attack(npc):
    interact(npc, 2)
fight = attack
a = attack

enabledcommands1 += ["interact", "talk", "speak", "t", "chat", "attack", "fight", "a"]
helpdb['interact'] = "Command aliases: 'interact'\nValid inputs: Creatures (friendly or otherwise) in the same room as you\nDescription: Begins an interaction with the input creature, in which you can attack them, talk to them, cast spells on them, or examine them via inputs on numbered submenus. When in an interaction, non-numbered commands will not work."
helpdb = {**helpdb, **dict.fromkeys(['talk', 'speak', 'chat', 't'], "Command aliases: 'talk', 'speak', 'chat', 't'\nValid inputs: Creatures (friendly or otherwise) in the same room as you\nDescription: Begins an interaction with the input creature (see 'interact' command), defaulting to the 'Talk' branch of the interaction.")}
helpdb = {**helpdb, **dict.fromkeys(['attack', 'fight', 'a'], "Command aliases: 'attack', 'fight', 'a'\nValid inputs: Creatures (friendly or otherwise) in the same room as you\nDescription: Begins an interaction with the input creature (see 'interact' command), defaulting to the 'Fight' branch of the interaction.")}

#################################
#   Cast and related commands   #
#################################

oneplacespells = ['flare', 'shield']

def cast(spellinput):
    if spellinput in oneplacespells:
        if spellinput in scripts.currprotag.spells:
            exec('print(interactions.'+spellinput+'(scripts.currprotag))')
    else:
        subdivision = parser2(spellinput, ['on', 'at'], 'cast')
        spell, target = subdivision[0], subdivision[1]
        if spell in scripts.currprotag.spells:
            if target == "me" or target == "self":
                exec('print(interactions.'+spell+'(scripts.currprotag))')
                if scripts.currprotag.dead:
                    print("You have died. Why did you do that?")
                return None
            else:
                for item in scripts.currprotag.location.contents:
                    if item.name.lower() == target:
                        exec('print(interactions.'+spell+'(item))')
                        if item.type == 'character':
                            interact(item.name.lower(), 3, True)
                        return None
                print("Could not find '"+target+"'.")
                return None
        print("You don't know any spell '"+spell+"'.")
spell = cast
c = cast

def flare():
    cast('flare')

def heal(target):
    cast('heal on '+target)

#Spell name here

#Spell name here

def disintegrate(target):
    cast('disintegrate on '+target)

def shield():
    cast('shield')

enabledcommands0 += ["flare", "shield"]
enabledcommands1 += ["cast", "spell", "c", "heal", "disintegrate"]
helpdb = {**helpdb, **dict.fromkeys(['cast', 'c'], "Command aliases: 'cast', 'spell, 'c', [name of spell]\nValid inputs: Known spells (use the 'self' command for a list of your known spells) and, if the spell used requires a target, objects or creatures in your vicinity (connected by the words 'on' or 'at', e.g. \"cast smelt at ore\"). Inputting 'me' or 'self' will attempt to cast the spell on yourself. If the input used was the name of a spell, the connector is unnecessary; instead, just input the target object or creature, e.g. \"smelt ore\"\nDescription: Attempts to cast the spell on the target, with effects varying from spell to spell. Note that, in addition to commands, the 'help' command can also offer information on the specific effects of spells.")}
helpdb['flare'] = ["Spell name: Flare\nValid inputs: None\nEffects: Creates a momentary flash of blinding light, potentially disorienting surrounding creatures."]
helpdb['heal'] = ["Spell name: Heal\nValid inputs: creatures in your vicinity, including yourself\nEffects: Heals the target creature for 10 health, up to a maximum of 100."]

#############
#   Debug   #
#############

#def exitparser():
#    scripts.running = False

#def die():
#    scripts.currprotag.die()

#def findwepon():
#    scripts.objects.wepon(scripts.currprotag.location)
#    pickup('wepon')
#    equip('wepon')

#def warp(target):
#    destinations = {'lair':scripts.world.lairentrance, 'shadow':scripts.world.shadowchamber, 'palace':scripts.world.shadowlair, 'melthar':scripts.world.throneroom}
#    if target in destinations:
#        scripts.currprotag.location = destinations[target]
#        destinations[target].contents.append(scripts.currprotag)
#        print("Warped to destination '"+target+"'.")
#    else:
#        print("Warp destination '"+target+"' not recognized. Please try again.")

#enabledcommands0 += ["exitparser", "die", "findwepon"]
#enabledcommands1 += ['warp']