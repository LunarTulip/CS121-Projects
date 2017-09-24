#This module contains all generation code for things which inherit from Object

import engine

###############
#   Objects   #
###############

def lairdoor(location, destination):
    lairdoor = engine.LockedDoor('Sturdy Door', location, 'south', destination)
    lairdoor.describe('You see a sturdy door on one of the buildings.', 'short')
    lairdoor.describe('A weathered but sturdy-looking wooden door. It has a keyhole sitting just above its steel doorknob.')
    return lairdoor

def shadowchamberdoor(location, destination):
    shadowchamberdoor = engine.LockedDoor('Blue Door', location, 'west', destination)
    shadowchamberdoor.describe('You see a high-tech door, painted blue.', 'short')
    shadowchamberdoor.describe('A door, made of some sort of blue-painted metal. It has a keycard reader to one side of it.')
    return shadowchamberdoor

def throneroomdoor(location, destination):
    throneroomdoor = engine.LockedDoor('Massive Door', location, 'north', destination)
    throneroomdoor.describe('You see a massive set of doors.', 'short')
    throneroomdoor.describe('An extremely large set of doors, almost twice as tall as anyone you\'ve ever met. It\'s covered in carvings depicting the founding of Nephosopolis.')
    return throneroomdoor

def blockade(location):
    blockade = engine.Object('Blockade', location)
    blockade.describe('You see a government blockade preventing you from taking the street any further north.', 'short')
    blockade.describe('A squadron of guards have established a wall across the street to the north, and now keep watch over it, ensuring that nobody attempts to climb it. You don\'t think it would be a good idea to get their attention.')
    return blockade

def ianessastatue(location):
    ianessastatue = engine.Object('Statue of Ianessa', location)
    ianessastatue.describe('You see a statue of Ianessa, the city\'s founder.', 'short')
    ianessastatue.describe('The cloud of which this statue has been constructed is beautifully worked, displaying none of the fraying around the edges that lesser statues might. It depicts Ianessa, the founder of Nephosopolis and arguably the greatest sorceress of all time, raising the city into the sky.')
    return ianessastatue

def laircrate(location):
    laircrate = engine.Container('Overturned Crate', location)
    laircrate.describe('You see a crate which has fallen on its side.', 'short')
    laircrate.describe('A wooden crate, lying on its side. The wood looks warped, and the crate\'s lid dangles limply by its hinges.')
    return laircrate

def bookshelf(location):
    bookshelf = engine.Object('Bookshelf', location)
    bookshelf.describe('You see a bookshelf which looks particularly frequently used', 'short')
    bookshelf.describe('This bookshelf appears particularly frequently used, judging by the haphazard state of the books on it. Flipping through them, it seems like Melthar was researching... sources of magic? That\'s interesting. You take a closer look.\n\nAccording to the first book you flip through, power granted by magical creatures is always focused through an object of some sort, and the destruction of that object will remove the user\'s power. You wonder what that implies about your own power, but more importantly, it means that Melthar could be beaten by figuring out what her focus is and destroying it. That\'s potentially very useful information.')
    return bookshelf

def shadowhorde(location):
    shadowhorde = engine.Object('Horde of Shadows', location)
    shadowhorde.describe('You see a mass of hungry-looking shadows in the darkness.', 'short')
    shadowhorde.describe('All around the island of light you stand in, shadows cover the walls. Seems like this is where Melthar is keeping all the shadows she was sending down the tunnel. You suspect that it would be a bad idea to step outside the light.')
    return shadowhorde

def celldoor(location):
    celldoor = engine.InternalDoor('Cell Door', location)
    celldoor.describe('You see a locked cell door.', 'short')
    celldoor.describe('A door comprised of thick steel bars in a grid pattern, with a large padlock preventing it from being opened.')
    return celldoor

def storeroomcrate(name, location):
    crate = engine.Container(name, location)
    crate.describe('You see a supply crate.', 'short')
    crate.describe('One of the many wooden crates piled up within the storeroom.')
    return crate

def shadowlocus(location):
    shadowlocus = engine.Object('Dark Sphere', location)
    shadowlocus.describe('You see a huge sphere of darkness floating in the middle of the room.')
    shadowlocus.describe('A huge sphere of darkness, with a diameter probably about as long as you are tall, floating in the middle of the room. It shifts menacingly as you look at it.')
    shadowlocus.spellresponse('flare', 'print("The sphere of darkness absorbs your flare. Nothing else happens.")')
    return shadowlocus

#############
#   Items   #
#############

def lairdoorkey(location):
    lairdoorkey = engine.Key('Windowless Building Key', location)
    lairdoorkey.describe('You see the key to the windowless building.', 'short')
    lairdoorkey.describe('A steel key, obtained from the housing office, which should be able to unlock the door to the windowless building in the dark alley.')
    return lairdoorkey

def shadowchamberkeycard(location):
    shadowchamberkeycard = engine.Key('Blue Keycard', location)
    shadowchamberkeycard.describe('You see a keycard with a blue stripe on it.', 'short')
    shadowchamberkeycard.describe('A white plastic keycard, with a thick blue stripe running perpendicular to the magnetic strip.')
    return shadowchamberkeycard

def throneroomkey(location):
    throneroomkey = engine.Key('Throne Room Key', location)
    throneroomkey.describe('You see a large platinum key.', 'short')
    throneroomkey.describe('A very large key, made of solid platinum. On its handle is an engraving of a cloud.')
    return throneroomkey

def celldoorkey(location):
    celldoorkey = engine.Key('Cell Door Keys', location)
    celldoorkey.describe('You see the keys to the dungeon\'s cells.', 'short')
    celldoorkey.describe('A weathered-looking ring of keys, most of which obviously match one or another of the locks in the dungeon\'s cells.')
    return celldoorkey

def shadowpasskey(location):
    shadowpasskey = engine.Item('Shadow Passkey', location)
    shadowpasskey.describe('You see a black keycard-looking item.', 'short')
    shadowpasskey.describe('A black card. It looks and feels a lot like a keycard, but you can feel a hum of magic around it which is definitely not present in typical keycards.')
    return shadowpasskey

def healthpotion(location):
    healthpotion = engine.Potion('Health Potion', location, 'interactions.healthpotion')
    healthpotion.describe('You see a health potion.', 'short')
    healthpotion.describe('A slightly glowing yellow liquid, held in a glass bottle. Drinking this will repair any injuries you may have accumulated. Its effects are stronger the more injured you are.')
    return healthpotion

###############
#   Weapons   #
###############

def lightningwand(location):
    lightningwand = engine.Weapon('Lightning Wand', location, 'Lightning Bolt', 'lightningbolt')
    lightningwand.describe('You see the wand from the pawn shop.', 'short')
    lightningwand.describe('A lavender-painted wand. It hums slightly with magical power, constantly occupying a small corner of your attention.')
    return lightningwand

def knife(location):
    knife = engine.Weapon('Knife', location, 'Slash (Knife)', 'knifeslash')
    knife.describe('You see a combat knife.', 'short')
    knife.describe('A combat knife. Short, sturdy, and sharp.')
    return knife

#############
#   Debug   #
#############

def wepon(location):
    wepon = engine.Weapon('wepon', location, 'shoot wepon', 'weponshoot')
    wepon.describe('wepon', 'short')
    wepon.describe('wepon')