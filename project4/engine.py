#This module contains all my classes

import interactions

#######################
#   General Library   #
#######################

class Library:
    def describe(self, description, type):
        if type == 'short':
            self.shortdesc = description
        else:
            self.description = description
    def spellresponse(self, spell, response):
        self.onspells[spell] = response

#############
#   Rooms   #
#############

oppositedirections = {'north':'south', 'south':'north', 'east':'west', 'west':'east', 'up':'down', 'down':'up'}

class Room:
    def __init__ (self):
        self.contents = []
        self.exits = {'north':None, 'south':None, 'east':None, 'west':None, 'up':None, 'down':None}
        self.onspells = {}
    def connect(self, room, direction): #Direction is direction of input room from commanded room, not inverse
        if self.exits[direction]: #If there's already a room connected in direction, disconnects it.
            self.exits[direction].exits[oppositedirections[direction]] = None
        for drctn in self.exits: #If room is already connected in a different direction, disconnects it.
            if self.exits[drctn] == room:
                room.exits[oppositedirections[drctn]] = None
                self.exits[drctn] = None
        self.exits[direction] = room
        room.exits[oppositedirections[direction]] = self
    def describe(self, description, type = None):
        Library.describe(self, description, type)
    def spellresponse(self, spell, response):
        Library.spellresponse(self, spell, response)

class SpecialRoom(Room):
    def __init__(self, loop):
        Room.__init__(self)
        self.loop = loop
        self.flags = {}

##################
#   Characters   #
##################

class Character:
    type = 'character'
    def __init__(self, name, room):
        self.name = name
        self.location = room
        self.inventory = {}
        self.onspells = {}
        self.dead = False
        room.contents.append(self)
    def move(self, direction):
        if direction in self.location.exits and self.location.exits[direction]:
            self.location.contents.remove(self)
            self.location.exits[direction].contents.append(self)
            self.location = self.location.exits[direction]
            result = "You move "+direction+"."
            if hasattr(self.location, 'shortdesc'):
                result += "\n"+self.location.shortdesc+"\n"
            activeexits = []
            for direction in self.location.exits:
                if self.location.exits[direction]:
                    activeexits.append(direction)
            if len(activeexits) >= 1:
                result += "\nYou see exits in the following directions:\n"
                for item in activeexits[:-1]:
                    result += item[0].upper()+item[1:]+", "
                result += activeexits[-1][0].upper()+activeexits[-1][1:]+"."
            else:
                result += "There are no exits visible."
            objects = []
            characters = []
            for item in self.location.contents:
                if item.type == 'character' and item != self:
                    characters.append(item)
                elif item != self:
                    objects.append(item)
            if len(objects) > 0 or len(characters) > 0:
                result += "\n"
            if len(objects) > 0:
                result += "\nYou see the following objects:"
                for item in objects:
                    result += "\n"+item.name
            if len(objects) > 0 and len(characters) > 0:
                result += "\n"
            if len(characters) > 0:
                result += "\nYou see the following creatures:"
                for item in characters:
                    result += "\n"+item.name
            return result
        else:
            return "There are no exits in direction '"+direction+"'."
    def pickup(self, itemname):
        for object in self.location.contents:
            if object.type == 'item' and object.name.lower() == itemname:
                if itemname in self.inventory:
                    self.inventory[itemname].append(object)
                else:
                    self.inventory[itemname] = [object]
                self.location.contents.remove(object)
                return "Picked up "+object.name+"."
            elif object.type != 'item' and object.name.lower() == itemname:
                return "Cannot pick up "+object.name+"."
        return "Could not find '"+itemname+"'."
    def drop(self, itemname):
        if itemname in self.inventory:
            self.location.contents.append(self.inventory[itemname][-1])
            returnval = "Dropped "+self.inventory[itemname][-1].name+"."
            del self.inventory[itemname][-1]
            if len(self.inventory[itemname]) == 0:
                del self.inventory[itemname]
            return returnval
        return "Could not find '"+itemname+"' in inventory."
    def die(self):
        self.location.contents.remove(self)
        for item in self.inventory:
            for i in range(len(self.inventory[item])):
                self.location.contents.append(self.inventory[item][i])
        self.dead = True
    def describe(self, description, type = None):
        Library.describe(self, description, type)
    def unlock(self, lockedthing):
        for object in self.location.contents:
            if object.name.lower() == lockedthing and hasattr(object, 'key'):
                for item in self.inventory:
                    if object.key in self.inventory[item]:
                        direction = None
                        if isinstance(object, LockedDoor):
                            direction = object.direction[0].upper()+object.direction[1:]
                        object.unlock()
                        itemname = self.inventory[item][0].name
                        self.inventory[item][0].consume(self)
                        result = "Unlocked "+object.name+" with "+itemname+"."
                        if direction:
                            result += " New exit opened in the following direction: "+direction+"."
                        return result
                return "You do not have a key capable of unlocking "+object.name+"."
            elif object.name.lower() == lockedthing:
                return object.name+" is not locked."
        return "Could not find '"+lockedthing+"'."
    def open(self, containername):
        for object in self.location.contents:
            if isinstance(object, Container) and object.name.lower() == containername:
                if object.opened:
                    return object.name+" is already open."
                else:
                    object.open()
                    if object.opened == True:
                        result = "Opened "+object.name+"."
                        if len(object.contents) == 0:
                            result += " It is empty."
                        else: #if len(object.contents > 0)
                            result += "\n\nIt contains the following items:"
                            for thing in object.contents:
                                if len(object.contents[thing]) == 1:
                                    result += "\n"+object.contents[thing][0].name
                                else: #len(object.contents[thing]) > 1
                                    result += "\n"+str(len(object.contents[thing]))+"x "+object.contents[thing][0].name
                        return result
                    else: #if object.opened == False
                        return object.name+" is locked."
            elif object.name.lower() == containername and hasattr(object, 'key'):
                return object.name+" is locked."
            elif object.name.lower() == containername:
                return object.name+" cannot be opened."
        return "Could not find '"+containername+"'."
    def close(self, containername):
        for object in self.location.contents:
            if isinstance(object, Container) and object.name.lower() == containername:
                if object.opened:
                    object.close()
                    return "Closed "+object.name+"."
                else:
                    return object.name+" is already closed."
            elif not isinstance(object, Container) and object.name.lower() == containername:
                return object.name+" cannot be closed."
        return "Could not find '"+containername+"'."
    def withdraw(self, itemname, containername):
        for object in self.location.contents:
            if isinstance(object, Container):
                if object.name.lower() == containername and object.opened == True:
                    if itemname in object.contents:
                        if itemname in self.inventory:
                            self.inventory[itemname].append(object.contents[itemname][-1])
                        else:
                            self.inventory[itemname] = [object.contents[itemname][-1]]
                        object.removeItem(self.inventory[itemname][-1])
                        return "Withdrew "+self.inventory[itemname][-1].name+" from "+object.name+"."
                    else:
                        return "Could not find "+itemname+" in "+containername+"."
                elif object.name.lower() == containername and object.opened == False:
                    return object.name+" is currently closed."
            elif object.name.lower() == containername:
                return object.name+" is not a container."
        return "Could not find container '"+containername+"'."
    def place(self, itemname, containername):
        if itemname in self.inventory:
            for object in self.location.contents:
                if isinstance(object, Container):
                    if object.name.lower() == containername and object.opened == True:
                        object.addItem(self.inventory[itemname][-1])
                        del self.inventory[itemname][-1]
                        if len(self.inventory[itemname]) == 0:
                            del self.inventory[itemname]
                        return "Placed "+object.contents[itemname][-1].name+" in "+object.name+"."
                    elif object.name.lower == containername and object.opened == False:
                        return object.name+" is currently closed."
                elif object.name.lower() == containername:
                    return object.name+" is not a container."
            return "Could not find container '"+containername+"'."
        return "Could not find "+itemname+" in inventory."
    def use(self, itemname):
        if itemname in self.inventory:
            if hasattr(self.inventory[itemname][0], "effect"):
                return self.inventory[itemname][0].use(self)
            else:
                return self.inventory[itemname][0].name+" is not a potion."
        else:
            return "Could not find item '"+itemname+"'."
    def spellresponse(self, spell, response):
        Library.spellresponse(self, spell, response)
    
class NPC(Character):
    def __init__(self, name, room, health, attack, pronoun, flags = None, hostile = False):
        Character.__init__(self, name, room)
        self.health = health
        self.talktree = Node({1:'Back'},{1:'self.curr, self.attackready = self.base, False'})
        self.attack = attack
        self.pronoun = pronoun
        self.hostile = hostile
        self.flags = flags
        self.overrides = {}
    def describe(self, description, type = None):
        if type == 'interaction':
            self.intdesc = description
        else:
            Library.describe(self, description, type)
    def addflag(self, flag, content):
        self.flags[flag] = content
    def addtalk(self, key, words, effect):
        self.talktree.add(key, words, effect)
    def deltalk(self, key):
        self.talktree.remove(key)
    def addpcdeathoverride(self, func):
        self.pcdeathoverride = func
    def addnpcdeathoverride(self, func):
        self.npcdeathoverride = func
    def setinteractloop(self, func):
        self.interactloop = func
    def setoverride(self, node, newdesc, newfunc): #Node is a string, not an int
        self.overrides[node] = [newdesc, newfunc]
    
class PC(Character):
    def __init__(self, name, room, health, spellnames, spells):
        Character.__init__(self, name, room)
        self.health = health
        self.gold = 0
        self.fighttree = Node({1:'Back', 2:'Punch'}, {1:'self.curr, self.attackready = self.base, False', 2:'print(interactions.punch(self.npc))'})
        self.spellnames = spellnames
        self.spells = spells
        self.casttree = Node({1:'Back', 2:spellnames[0], 3:spellnames[1]}, {1:'self.curr, self.attackready = self.base, False', 2:'print(interactions.'+spells[0]+'(self.npc))', 3:'print(interactions.'+spells[1]+'(self.npc))'})
        self.shielded = False
        self.weapon1 = None
        self.weapon2 = None
        self.won = False
    def equip(self, weapon):
        if weapon in self.inventory:
            if self.weapon1 == None:
                equipslot = 1
            elif self.weapon2 == None:
                equipslot = 2
            else:
                print('Would you like to equip '+self.inventory[weapon][0].name+' in place of '+weapon1.name+' or in place of '+weapon2.name+'?>')
                print('1: '+self.weapon1.name+'\n2: '+self.weapon2.name+'\n3: Never mind')
                equipslot = input('>')
                while not (equipslot.isdigit() and int(equipslot) in [1, 2, 3]):
                    print('Please input one of the listed numbers.')
                    choice = input('\n>')
            if equipslot == 1:
                self.weapon1 = self.inventory[weapon][0]
                self.fighttree.add(3, self.weapon1.attackdesc, 'print(interactions.'+self.weapon1.attack+'(self.npc))')
                return 'Equipped '+self.inventory[weapon][0].name+'.'
            elif equipslot == 2:
                self.weapon2 = self.inventory[weapon][0]
                self.fighttree.add(4, self.weapon2.attackdesc, 'print(interactions.'+self.weapon2.attack+'(self.npc))')
                return 'Equipped '+self.inventory[weapon][0].name+'.'
            else: #equipslot == 3
                return 'Did not equip '+self.inventory[weapon][0].name+'.'
        else:
            return "cannot find '"+weapon+"' in inventory."

###############
#   Objects   #
###############

class Object:
    type = 'object'
    def __init__(self, name, location = None):
        self.name = name
        self.onspells = {}
        if location:
            self.location = location
            self.location.contents.append(self)
    def describe(self, description, type = None):
        Library.describe(self, description, type)
    def spellresponse(self, spell, response):
        Library.spellresponse(self, spell, response)

class Container(Object):
    def __init__(self, name, location):
        Object.__init__(self, name, location)
        self.contents = {}
        self.opened = False
    def addItem(self, item):
        if item.name.lower() in self.contents:
            self.contents[item.name.lower()].append(item)
        else:
            self.contents[item.name.lower()] = [item]
    def removeItem(self, item):
        del self.contents[item.name.lower()][-1]
        if len(self.contents[item.name.lower()]) == 0:
            del self.contents[item.name.lower()]
    def open(self):
        self.opened = True
    def close(self):
        self.opened = False

class LockedContainer(Container):
    def __init__(self, name, location):
        Container.__init__(self, name, location)
        self.locked = True
        self.key = None
    def open(self):
        if not self.locked:
            self.opened = True
    def unlock(self):
        self.locked = False

class LockedDoor(Object):
    def __init__(self, name, location, direction, destination):
        Object.__init__(self, name, location)
        self.direction = direction
        self.destination = destination
        self.key = None
    def unlock(self):
        self.location.connect(self.destination, self.direction)
        self.location.contents.remove(self)

class InternalDoor(Object):
    def __init__(self, name, location):
        Object.__init__(self, name, location)
        self.key = None
    def unlock(self):
        self.location.contents.remove(self)

class Item(Object):
    type = 'item'
    def consume(self, user):
        for item in user.inventory:
            if self.name.lower() in user.inventory:
                del user.inventory[self.name.lower()][-1]
                if len(user.inventory[self.name.lower()]) == 0:
                    del user.inventory[self.name.lower()]
                    return None

class Key(Item):
    def attune(self, object):
        object.key = self

class Weapon(Item):
    def __init__(self, name, location, attackdesc, attack):
        Item.__init__(self, name, location)
        self.attack = attack
        self.attackdesc = attackdesc

class Potion(Item):
    def __init__(self, name, location, effect):
        Item.__init__(self, name, location)
        self.effect = effect
    def use(self, user):
        return eval(self.effect+"(self, user)")

##############################
#   The Interaction System   #
##############################

class Node: #Basics of data structure: each node has a set of numbers as keys, each associated with a description and a contents. The description is a string describing the contents. The contents are either another node or a function.
    def __init__(self, descriptions = {}, contents = {}):
        self.descriptions = descriptions
        self.contents = contents
    def add(self, key, description, contents):
        self.descriptions[key] = description
        self.contents[key] = contents
    def remove(self, key):
        del self.descriptions[key]
        del self.contents[key]

class Interaction:
    def __init__(self, pc, npc, entrypoint = None):
        self.base = Node({1:'Talk', 2:'Fight', 3:'Cast', 4:'Examine', 5:'Leave'}, {1:npc.talktree, 2:pc.fighttree, 3:pc.casttree, 4:'print(interactions.examine(self.npc))', 5:'self.running = False'})
        if len(npc.overrides) > 0:
            for override in npc.overrides:
                focus = self.base
                topic = int(override)
                if "." in override: #Allows overrides to affect subnodes rather than only root nodes
                    branch = override[:override.index(".")]
                    topic = override[override.index(".") + 1:]
                    focus = self.base.contents[int(branch)]
                focus.descriptions[topic] = npc.overrides[override][0]
                focus.contents[int(override)] = npc.overrides[override][1]
        if entrypoint:
            self.curr = self.base.contents[entrypoint]
        else:
            self.curr = self.base
        self.submenu = 0
        self.pc = pc
        self.npc = npc
        self.pcdeath = 'print(interactions.pcdeath(self.pc))'
        self.npcdeath = 'print(interactions.npcdeath(self.npc))'
        self.checkonloop = 'None'
        if hasattr(npc, 'pcdeathoverride'):
            self.pcdeath = npc.pcdeathoverride
        if hasattr(npc, 'npcdeathoverride'):
            self.npcdeath = npc.npcdeathoverride
        if hasattr(npc, 'interactloop'):
            self.checkonloop = npc.interactloop
        self.running = True
        self.attackready = False
    def interact(self, key):
        if isinstance(self.curr.contents[key], Node):
            self.submenu = key
            self.curr = self.curr.contents[key]
        else: #self.curr.contents[key] is a command
            if self.npc.hostile:
                self.attackready = True
            exec(self.curr.contents[key])
            self.checkloop()
            if self.attackready and self.npc.hostile and not (self.npc.dead or self.npc.health <= 0):
                print()
                print(self.npc.attack(self.npc, self.pc))
                self.checkdeath()
    def checkdeath(self):
        if self.pc.health <= 0 or self.pc.dead:
            self.running = False
            exec(self.pcdeath)
        elif self.npc.health <= 0 or self.npc.dead:
            self.running = False
            exec(self.npcdeath)
        else: #Neither dead
            return 'checkloop'
    def checkloop(self):
        if self.checkdeath() == 'checkloop':
            exec(self.checkonloop)