#This module generates and keeps track of the state of the game and the world

import rooms
import characters
import objects

running = True #Variable controlling if the parser is on; mainly for debug purposes
currprotag = None #Variable controlling the identity of the PC; must have a value for game to be playable.

class World:
    def start(self): #Initializes the world for Raelina
        
        global currprotag
        
        #############
        #   Rooms   #
        #############
        
        self.nessstreetsouth = rooms.nessstreetsouth()
        self.nessstreetnorth = rooms.nessstreetnorth()
        self.housingoffice = rooms.housingoffice()
        self.pawnshop = rooms.pawnshop()
        self.residentialarea = rooms.residentialarea()
        self.janalshousedown = rooms.janalshousedown()
        self.janalshouseup = rooms.janalshouseup()
        self.darkalley = rooms.darkalley()
        self.abandonedbuilding = rooms.abandonedbuilding()
        self.lairentrance = rooms.lairentrance()
        self.laircenter = rooms.laircenter()
        self.library = rooms.library()
        self.shadowchamber = rooms.shadowchamber()
        self.shadowtunnel = rooms.shadowtunnel()
        self.palacebasement = rooms.palacebasement()
        self.shadowlair = rooms.shadowlair()
        self.dungeon = rooms.dungeon()
        self.wardensoffice = rooms.wardensoffice()
        self.stairwellbottom = rooms.stairwellbottom()
        self.stairwelltop = rooms.stairwelltop()
        self.palacehallway = rooms.palacehallway()
        self.barracks = rooms.barracks()
        self.storeroom = rooms.storeroom()
        self.throneroomentry = rooms.throneroomentry()
        self.throneroom = rooms.throneroom()
        
        self.nessstreetsouth.connect(self.nessstreetnorth, 'north')
        self.nessstreetnorth.connect(self.housingoffice, 'west')
        self.nessstreetnorth.connect(self.pawnshop, 'east')
        self.nessstreetsouth.connect(self.residentialarea, 'east')
        self.residentialarea.connect(self.janalshousedown, 'north')
        self.janalshousedown.connect(self.janalshouseup, 'up')
        self.nessstreetsouth.connect(self.darkalley, 'west')
        self.abandonedbuilding.connect(self.lairentrance, 'down')
        self.lairentrance.connect(self.laircenter, 'north')
        self.laircenter.connect(self.library, 'east')
        self.shadowtunnel.connect(self.shadowtunnel, 'north')
        self.shadowchamber.connect(self.shadowtunnel, 'north')
        self.shadowtunnel.flags['destination'] = self.palacebasement
        self.palacebasement.connect(self.shadowlair, 'up')
        self.shadowlair.connect(self.dungeon, 'up')
        self.dungeon.connect(self.wardensoffice, 'east')
        self.dungeon.connect(self.stairwellbottom, 'west')
        self.stairwellbottom.connect(self.stairwelltop, 'up')
        self.stairwelltop.connect(self.palacehallway, 'north')
        self.palacehallway.connect(self.barracks, 'west')
        self.palacehallway.connect(self.storeroom, 'east')
        self.palacehallway.connect(self.throneroomentry, 'north')
        
        self.scriptroom = rooms.scriptroom()
        self.scriptroom.exits['up'] = self.shadowtunnel
        self.scriptroom.exits['down'] = self.storeroom
        
        ##################
        #   Characters   #
        ##################
        
        currprotag = characters.raelina(self.nessstreetsouth)
        self.beggar = characters.beggar(self.nessstreetsouth)
        self.housingmanager = characters.housingmanager(self.housingoffice)
        self.shopkeeper = characters.shopkeeper(self.pawnshop)
        self.janal = characters.janal(self.janalshousedown)
        self.wrynn = characters.wrynn(self.janalshouseup)
        self.janal.flags['wife'], self.wrynn.flags['wife'] = self.wrynn, self.janal
        self.shadowaccumulator = characters.shadowaccumulator(self.shadowchamber)
        self.prisoner = characters.prisoner(self.dungeon)
        self.warden = characters.warden(self.wardensoffice)
        self.guard = characters.guard(self.barracks)
        self.throneroomguards = characters.throneroomguards(self.throneroomentry)
        self.guard.flags['shadowguards'] = self.throneroomguards
        self.melthar = characters.meltharnpc(self.throneroom)
        self.warden.flags['melthar'] = self.melthar
        
        self.tunnelshadow = characters.shadow(self.scriptroom)
        self.shadowtunnel.flags['shadow'] = self.tunnelshadow
        self.storeroomshadows = []
        for i in range(6):
            self.storeroomshadows.append(characters.shadow(self.scriptroom))
        self.storeroom.flags['shadows'] = self.storeroomshadows
        
        ###############
        #   Objects   #
        ###############
        
        self.lairdoor = objects.lairdoor(self.darkalley, self.abandonedbuilding)
        self.lairdoorkey = objects.lairdoorkey(self.housingoffice)
        self.lairdoorkey.attune(self.lairdoor)
        self.shadowchamberdoor = objects.shadowchamberdoor(self.laircenter, self.shadowchamber)
        self.shadowchamberkeycard = objects.shadowchamberkeycard(None)
        self.shadowchamberkeycard.attune(self.shadowchamberdoor)
        self.celldoor = objects.celldoor(self.dungeon)
        self.celldoorkey = objects.celldoorkey(self.wardensoffice)
        self.celldoorkey.attune(self.celldoor)
        self.throneroomdoor = objects.throneroomdoor(self.throneroomentry, self.throneroom)
        self.throneroomkey = objects.throneroomkey(self.throneroomentry)
        self.throneroomkey.attune(self.throneroomdoor)
        
        self.blockade = objects.blockade(self.nessstreetnorth)
        self.ianessastatue = objects.ianessastatue(self.residentialarea)
        self.lightningwand = objects.lightningwand(self.pawnshop)
        self.knife = objects.knife(None)
        self.bookshelf = objects.bookshelf(self.library)
        self.shadowhorde = objects.shadowhorde(self.shadowlair)
        self.prisonerpotion = objects.healthpotion(self.dungeon)
        self.shadowpasskey = objects.shadowpasskey(self.barracks)
        self.shadowlocus = objects.shadowlocus(self.throneroom)
        self.melthar.flags['shadowlocus'] = self.shadowlocus
        
        self.housingmanager.pickup('windowless building key')
        self.shopkeeper.pickup('lightning wand')
        self.prisoner.pickup('health potion')
        self.warden.pickup('cell door keys')
        self.guard.pickup('shadow passkey')
        self.throneroomguards.pickup('throne room key')
        
        self.laircrate = objects.laircrate(self.lairentrance)
        self.laircrate.addItem(self.shadowchamberkeycard)
        self.laircrate.addItem(self.knife)
        self.potioncrate2 = objects.storeroomcrate('Generic Crate', self.storeroom) #Crates out of order here so they're out of order in the room's contents list
        for i in range(2):
            self.potioncrate2.addItem(objects.healthpotion(None))
        self.potioncrate1 = objects.storeroomcrate('Unidentified Crate', self.storeroom)
        self.potioncrate1.addItem(objects.healthpotion(None))
        self.emptycrate = objects.storeroomcrate('Anonymous Crate', self.storeroom)
        self.potioncrate3 = objects.storeroomcrate('Mysterious Crate', self.storeroom)
        for i in range(3):
            self.potioncrate3.addItem(objects.healthpotion(None))

        ####################
        #   Introduction   #
        ####################
        
        #Commented-out lines are from the original draft, kept in just in case they turn out to be useful to copy from at some later date
        
        print("Your name is Raelina. A month ago, your hometown of Nephosopolis was, seemingly out of nowhere, taken over by a sorceress calling herself Queen Melthar following the assassination of dozens of top government officials.\n")
        #print("Your name is Raelina. Two months ago, your hometown of Nephosopolis was, seemingly out of nowhere, taken over by a sorceress calling herself Queen Melthar following the assassination of dozens of top government officials.\n")
        print("A few weeks after that, you were contacted by a strange creature which offered you magical powers of your choosing in exchange for your using those powers to fight back against Melthar and against the shadow monster that it claimed was backing her.\n")
        #print("A few weeks after that, you and your two sisters were contacted by a strange creature which offered the three of you magical powers of your choosing in exchange for your using those powers to fight back against Melthar and against the shadow monster that it claimed was backing her.\n")
        print("You accepted immediately, asking for power over light, because that seemed likely to be helpful in fighting shadow monsters. Now, you're on the hunt for any leads on how to beat Queen Melthar.\n")
        #print("You accepted immediately, asking for power over light, because what else would you want when you're fighting shadow monsters? Your younger sister Sarille asked for the power of knowledge, which... yes, it's useful, but you don't really see how it's applicable to the current situation. And you never learned what your older sister Lanise asked for; she requested it in secret, and refuses to discuss it with you or your sister, instead having remained shut up in her room almost constantly since then.\n")
        #print("That was over a month ago. Your sisters keep wasting their time planning, as if better options are just going to magically drop in their lap if they wait long enough. You've already had literal magic dropped in your laps; you're not going to get any better than that, and the longer you wait the longer Melthar has to advance whatever plans she's working on. You haven't been able to talk them out of it. So, instead, you're going in alone.\n")
        #print("You are now on the southern end of Ness Street, looking for Melthar's hideout. You know she spends her time at the palace now, but wherever she was hiding out before her takeover is where you most expect to find something that could lead you to defeat her, and you've heard rumors of strange shadow monsters stalking this region at night. It seems like the ideal place to start.\n")
        print("You've heard rumors of strange shadow monsters stalking this region at night. It seems like the ideal place to start. You are currently on the southern end of Ness Street. To the west, you see a narrow and dark-looking alleyway. To the east, you see a side street leading to a residential block. To the north, Ness Street continues; you recall it enters a commercial district. Standing nearby is a beggar. Perhaps you could ask him about the rumors you've heard?\n")
        print("(To see a list of available commands, type 'help'. To see the detailed usage and aliases of a specific command, type 'help [command name]'. Have fun!)\n")
        print("You see exits in the following directions:\nNorth, East, West.\n\nYou see the following creatures:\nBeggar")
        
    def raelinadead(self): #Updates the world for Sarille
        pass
    def sarilledead(self): #Updates the world for Lanise
        pass
    def lanisedead(self): #Updates the world for Melthar
        pass