#This module contains all generation code for things which inherit from Room

import engine

###############
#   Streets   #
###############

def nessstreetsouth():
    nessstreetsouth = engine.Room()
    nessstreetsouth.describe('You return to the southern end of Ness Street. The street continues to the north. To the east, you see a small residential offshoot street. To the west is a narrow dark-looking alley.', 'short')
    nessstreetsouth.describe('The southern end of Ness Street, where the street begins to intersect with local residential roads.')
    return nessstreetsouth

def nessstreetnorth():
    nessstreetnorth = engine.Room()
    nessstreetnorth.describe('You move to the northern end of Ness Street. To the west, you see the local housing office. To the east, you see a pawn shop. You can also return south.', 'short')
    nessstreetnorth.describe('The northern end of Ness Street, covered in shops of various descriptions.')
    return nessstreetnorth

def housingoffice():
    housingoffice = engine.Room()
    housingoffice.describe('You enter the housing office.', 'short')
    housingoffice.describe('An official government housing office, in charge of allocating and collecting keys to houses in this region.')
    return housingoffice

def pawnshop():
    pawnshop = engine.Room()
    pawnshop.describe('You enter the pawn shop.', 'short')
    pawnshop.describe('A family-owned pawn shop. The shelves are covered in assorted objects. Seems like they\'ve been getting a lot of sellers lately.')
    return pawnshop

def residentialarea():
    residentialarea = engine.Room()
    residentialarea.describe('You enter a side street dotted with small houses. One house to the north has a large sign on the door: "HELP WANTED!"', 'short')
    residentialarea.describe('One of Ness Street\'s many residential side streets. Small houses dot either side of the street, packed tightly together.')
    return residentialarea

def janalshousedown():
    janalshousedown = engine.Room()
    janalshousedown.describe('You enter a modest sitting room. There is a staircase leading up.', 'short')
    janalshousedown.describe('A sitting room, with three chairs and a table, along with a staircase in the corner leading upwards.')
    return janalshousedown

def janalshouseup():
    janalshouseup = engine.Room()
    janalshouseup.describe('You enter the house\'s upper floor.', 'short')
    janalshouseup.describe('The upstairs portion of the house is a single large room, without any walls to divvy it up. It seems like this is where they sleep, judging by the mattresses on the floor.')
    return janalshouseup

def darkalley():
    darkalley = engine.Room()
    darkalley.describe('You enter a dark alley. To the south, you see a windowless building with a sturdy-looking door.', 'short')
    darkalley.describe('The houses here are packed tightly together, blocking most of the sunlight, and none of the houses\' own lights are on, creating an overall dark atmosphere.')
    return darkalley

def abandonedbuilding():
    abandonedbuilding = engine.Room()
    abandonedbuilding.describe('You enter the windowless building. You see a trapdoor embedded in the floor.', 'short')
    abandonedbuilding.describe('This building is almost completely stripped clean, and has clearly been empty for at least a month or two. Dust piles on every surface, except where you kick it into the air.')
    return abandonedbuilding

############
#   Lair   #
############

def lairentrance():
    lairentrance = engine.Room()
    lairentrance.describe('You enter what you hope to be Queen Melthar\'s lair. It is as delapidated as the house above.', 'short')
    lairentrance.describe('A small hallway, with a ladder at one end leading back to the house above. The dust is as thick here as it was there, and the atmosphere far thicker.')
    return lairentrance

def laircenter():
    laircenter = engine.Room()
    laircenter.describe('You enter a large living area.', 'short')
    laircenter.describe('A large room, with a few couches, a few desks with some books scattered across them, and even an oven and stove in the corner. The floor and couches are periodically stained with blood, spoiling any homey mood the room may otherwise have had.')
    return laircenter

def library():
    library = engine.Room()
    library.describe('You enter a library, covered in shelves filled to the brim with books.', 'short')
    library.describe('Shelves cover the room\'s walls from one side to another. You don\'t recognize any of the books, but you\'re sure your sister would love this place.')
    return library

def shadowchamber():
    shadowchamber = engine.Room()
    shadowchamber.describe('You enter a room containing some sort of dark magical apparatus.', 'short')
    shadowchamber.describe('An elaborate laboratory, covered in tools and tubing.')
    return shadowchamber

def shadowtunnel():
    shadowtunnel = engine.SpecialRoom('interactions.shadowtunnelscary(scripts.currprotag, scripts.world.shadowtunnel)')
    shadowtunnel.describe('You enter the tunnel the shadows were being sent down. It is very dark.', 'short')
    shadowtunnel.describe('The walls of this tunnel seem to absorb all light that comes into them, rendering the area supernaturally dark. It continues to run north, but you can\'t tell how far in this darkness.')
    shadowtunnel.flags = {'warning1':False, 'warning2':False, 'warning3':False, 'pacified':False, 'destination':None, 'shadow':None}
    shadowtunnel.spellresponse('flare', 'shadowtunnelflare()')
    return shadowtunnel

def palacebasement():
    palacebasement = engine.Room()
    palacebasement.describe('After walking for almost twenty minutes, you finally reach a small room with a ladder leading upwards.', 'short')
    palacebasement.describe('A small room containing a ladder and not much else. You see a trapdoor of some sort above the ladder, with holes in it allowing you to see glimpses of a bright light on the other side.')
    return palacebasement

##############
#   Palace   #
##############

def shadowlair():
    shadowlair = engine.Room()
    shadowlair.describe('You emerge into a small cone of very bright light. All around you is shadow. There are two ladders next to you, one going down and one going up.', 'short')
    shadowlair.describe('A narrow cone of light, blasted by an array of spotlights in the ceiling, keeps the area immediately around the room\'s ladders lit. The entire rest of the room is dark.')
    return shadowlair

def dungeon():
    dungeon = engine.SpecialRoom('interactions.dungeondoorcheck(scripts.world.celldoor, scripts.world.prisoner, scripts.currprotag)')
    dungeon.describe('You enter an underground prison.', 'short')
    dungeon.describe('Barred cells cover the northern and southern walls of the hallway you\'re standing in.')
    dungeon.flags = {'dooropened':False}
    return dungeon

def wardensoffice():
    wardensoffice = engine.Room()
    wardensoffice.describe('You enter a warmly-lit office.', 'short')
    wardensoffice.describe('This room, while small, looks homier than the entire set of cells to the west put together. A fire crackles in a fireplace on one wall, and papers litter the desk in the middle of the room.')
    return wardensoffice

def stairwellbottom():
    stairwellbottom = engine.SpecialRoom('interactions.palacerealization(scripts.world.stairwellbottom)')
    stairwellbottom.describe('You reach the bottom of a staircase.', 'short')
    stairwellbottom.describe('A round cloudstone room, with a spiral staircase running up along the edges.')
    stairwellbottom.flags = {'realized':False}
    return stairwellbottom

def stairwelltop():
    stairwelltop = engine.Room()
    stairwelltop.describe('You reach the top of a staircase.', 'short')
    stairwelltop.describe('A round cloudstone room, with a spiral staircase running down from one side.')
    return stairwelltop

def palacehallway():
    palacehallway = engine.Room()
    palacehallway.describe('You reach a crossroads in the palace\'s halls. To the west is a large-but-empty-looking room; to the north and west the hall runs further.', 'short')
    palacehallway.describe('The clouds that make up this hallway have torches periodically embedded in them. The torches glow with blue fire, and there\'s no obvious mechanism for replacing them. Powered by dark magic, you presume.')
    return palacehallway

def barracks():
    barracks = engine.SpecialRoom('interactions.barracksentry(scripts.world.barracks)')
    barracks.describe('You enter a barracks.', 'short')
    barracks.describe('A barracks. Beds tile the parts of the room near the walls, each with a locked chest at their foot. In the middle of the room is a circular table, large enough that you could imagine the owners of every one of those beds all squeezed around it at once.')
    barracks.flags = {'entered':False}
    return barracks

def storeroom():
    storeroom = engine.SpecialRoom('interactions.storeroomshadows(scripts.currprotag, scripts.world.storeroom)')
    storeroom.describe('You enter a room filled to the brim with crates of various goods.', 'short')
    storeroom.describe('Crates are piled almost to the ceiling in this room, each with a transparent panel on its side to let you see inside. Judging by the strange patterns of light along the walls and ceiling, there are shadows patrolling the room.')
    storeroom.flags = {'shadows':None, 'firstentry':True, 'usedpasskey':False, 'roomcleared':False}
    return storeroom

def throneroomentry():
    throneroomentry = engine.Room()
    throneroomentry.describe('You reach the end of the hallway, and find it barred by a massive set of doors.', 'short')
    throneroomentry.describe('The end of the hallway you\'ve been traveling down. On the northern end is the doorway to the throne room; to the south is the way you came.')
    return throneroomentry

def throneroom():
    throneroom = engine.SpecialRoom('interactions.throneroomentry(scripts.currprotag, scripts.world.melthar)')
    throneroom.describe('You enter Queen Melthar\'s throne room.', 'short')
    throneroom.describe('Queen Melthar\'s throne room. Finally, you\'ve made it here. Now all that\'s left is to stop her once and for all.')
    throneroom.flags = {'entered':False}
    return throneroom

#############
#   Other   #
#############

def scriptroom():
    scriptroom = engine.Room()
    return scriptroom