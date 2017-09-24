#This module contains effects run in response to environmental cues or player interactions that aren't directly commands

import random
import commands

##############
#   Engine   #
##############

def examine(target):
    if hasattr(target, 'intdesc'):
        return target.intdesc
    else:
        return target.description

def pcdeath(pc):
    pc.die()
    return "\nYou have died."

def npcdeath(npc):
    result = "\n"+npc.name+" has died."
    if len(npc.inventory) > 0:
        result += "\n\n"+npc.pronoun+" drops the following items:\n"
        for item in npc.inventory:
            if len(npc.inventory[item]) == 1:
                result += "\n"+npc.inventory[item][0].name
            else: #len(npc.inventory[item]) > 1
                result += "\n"+str(len(npc.inventory[item]))+"x "+npc.inventory[item][0].name
        result += "\n"
    npc.die()
    return result

def pcwin(pc):
    pc.won = True

##############
#   Spells   #
##############

#Only the first two spells are actually in use in the final game; the others are from prior more-ambitious versions

def flare(pc):
    effects = False
    print("You let out a blinding flash of light. ", end='')
    for item in pc.location.contents:
        if 'flare' in item.onspells:
            effects = True
            exec(item.onspells['flare'])
            return ""
    if not effects:
        if 'flare' in pc.location.onspells:
            effects = True
            exec(pc.location.onspells['flare'])
            return ""
    if not effects:
        return "Nothing interesting happens."

def heal(target):
    if hasattr(target, 'health'):
        if target.health < 100:
            start = target.health
            target.health += 10
            if target.health > 100:
                target.health = 100
            amounthealed = target.health - start
            if hasattr(target, 'pronoun'):
                return "Healed "+target.name+" for "+str(amounthealed)+" health. "+target.pronoun+" now has a total of "+str(target.health)+" health."
            else:
                return "Healed yourself for "+str(amounthealed)+" health. You now have a total of "+str(target.health)+" health."
        elif hasattr(target, 'pronoun'):
            return target.name+" is already very healthy. "+target.pronoun+" can't be healed any further."
        else: #not hasattr(target, 'pronoun'):
            return "You are already very healthy. You can't heal yourself any further."
    else:
        return target.name+" is not alive, and thus cannot be healed."

#def read(target):
    #Given an NPC target, reads their mind, potentially giving useful hints

#def scry(target):
    #Given a closed chest or a locked door, shows the contents or the destination
    #Possibly too useless? Figure out a way to make it good

def disintegrate(target):
    if 'disintegrate' in target.onspells:
        exec(target.onspells['disintegrate'])
    else:
        result = "Disintegrated "+target.name+"."
        if hasattr(target, 'key') and hasattr(target, 'direction'):
            result += " New exit opened in the following direction: "+target.direction[0].upper()+target.direction[1:]+"."
            target.unlock()
        else:
            target.location.contents.remove(target)
            if target.type == 'character':
                target.dead = True
        return result

def shield(pc):
    pc.shielded = True
    return "You form a magical shield around yourself."

##################
#   PC Attacks   #
##################

def punch(target):
    target.health -= 5
    result = "Punched "+target.name+". "+target.pronoun+" has "+str(target.health)+" health remaining."
    if hasattr(target, "hostile") and target.hostile == False:
        target.hostile = True
        result += " "+target.name+" is now hostile."
    return result

def knifeslash(target):
    target.health -= 10
    result = "Slashed "+target.name+" with knife. "+target.pronoun+" has "+str(target.health)+" health remaining."
    if hasattr(target, "hostile") and target.hostile == False:
        target.hostile = True
        result += " "+target.name+" is now hostile."
    return result

def lightningbolt(target):
    target.health -= 15
    result = "You shoot a blast of lightning at "+target.name+". "+target.pronoun+" has "+str(target.health)+" health remaining."
    if hasattr(target, "hostile") and target.hostile == False:
        target.hostile = True
        result += " "+target.name+" is now hostile."
    return result

###################
#   NPC Attacks   #
###################

def npcpunch(npc, pc):
    pc.health -= 5
    return npc.name+" punches you. You have "+str(pc.health)+" health remaining."

def npcflail(npc, pc):
    return npc.name+" flails weakly at you, but fails to hurt you in any way."

def nonattack(npc, pc):
    return npc.name+" makes no attempt to attack you."

def shadowattack(npc, pc):
    pc.health -= 15
    return "The shadow envelops you for a moment, and you feel it tearing at your skin. You have "+str(pc.health)+" health remaining."

def toolwhirlwind(npc, pc):
    pc.health -= random.randint(5, 14)
    return "You are bludgeoned by a whirlwind of lab equipment. You have "+str(pc.health)+" health remaining."

def npcsword(npc, pc):
    pc.health -= 10
    return npc.name+" slashes at you with a sword. You have "+str(pc.health)+" health remaining."

def shadowguardsatt(npc, pc):
    pc.health -= 20
    return "The guards slash at you with their swords from multiple directions at once. It's very difficult to defend against. You have "+str(pc.health)+" health remaining."

def meltharcombat(npc, pc):
    choice = random.randint(1, 5)
    if choice <= 2:
        pc.health -= 15
        return "The sphere of darkness behind Melthar blasts you with energy. You have "+str(pc.health)+" health remaining."
    elif choice <= 4:
        pc.health -= random.randint(10, 20)
        return "You are enveloped in a whirlwind of shadows, which cuts at every bit of exposed skin that it touches. You have "+str(pc.health)+" health remaining."
    else: #choice = 5
        pc.health -= 10
        npc.health += 10
        return "Melthar leeches some life force from you. You have "+str(pc.health)+" health remaining. Melthar now has "+str(npc.health)+" health remaining."

####################
#   Item Effects   #
####################

def healthpotion(potion, pc):
    startinghealth = pc.health
    pc.health += 10 + (10 - (pc.health // 10))
    potion.consume(pc)
    return "Drunk health potion. "+str(pc.health - startinghealth)+" health restored. You now have "+str(pc.health)+" health remaining."

############################
#   Conversation Effects   #
############################

def helpbeggar(pc, npc):
    if pc.gold >= 2:
        pc.gold -= 2
        print('You give the beggar two gold. He gives you an enormous grin. Seems like you\'ve made his day.')
        npc.describe('The beggar now smiles broadly whenever he looks at you.', 'interaction')
    else:
        print('You reach for money to give the beggar, but find your pouch empty. Guess you can\'t do that after all.')

def askforkey(pc, npc):
    print('"Sure," he says, looking surprised to find you actually buying something in the current climate. "If you\'re sure, then that\'ll be thirty gold."')
    if pc.gold >= 30:
        buychoice = input('\nBuy the key? Y/N\n>').lower()
        if buychoice == 'y' or buychoice == 'yes':
            pc.gold -= 30
            npc.drop('windowless building key')
            pc.pickup('windowless building key')
            print('You give him thirty gold, and he gives you the key. Windowless Building Key acquired.')
            npc.deltalk(2)
        else:
            print('You choose not to buy the key. He sighs and returns to his paperwork.')
    else:
        print('\nYou don\'t have enough gold, but you tell him you might come back when you do. He sighs and nods.')

def findwand(pc, npc):
    print("He shows you a large number of trinkets of no relevance to your current quest. Just when you're about to write his shop off as a lost cause, you see a genuinely powerful-looking magic wand.")
    npc.addtalk(3, 'Ask to buy the wand (15 gold)', 'interactions.buywand(self.pc, self.npc)')

def buywand(pc, npc):
    if pc.gold >= 15:
        pc.gold -= 15
        npc.drop('lightning wand')
        pc.pickup('lightning wand')
        print('You buy the wand for fifteen gold. After a few moments of testing, you determine that it can shoot lightning bolts. Lightning Wand acquired.')
        npc.deltalk(3)
    else:
        print('You don\'t have enough gold.')

def janalqueststart(pc, npc):
    print("She tells you that her wife Wrynn has fallen mysteriously sick over the last month or so, and that she\'s been looking for anyone who knows enough to possibly cure her.")
    pchelps = input('\nDo you offer to try to help? Y/N\n>').lower()
    if pchelps == 'yes' or pchelps == 'y':
        print('"Thank you!" she says, her eyes lighting up. "You can find her upstairs."')
        npc.addtalk(2, "Ask how she's holding up", "print('\"Fine,\" she says, \"but constantly worried about Wrynn. Please work quickly.')")
        npc.flags['wife'].addtalk(2, "Ask what's been tried so far to heal her", 'print("She takes in a deep breath, then tells you that she\'s been tested for every disease any doctors could think of, and not been found to have any of them. The only hope she has left is for Janal to find a magical solution, but with how rare magic is, she doubts Janal will make it in time. You tell her that you actually can cast healing magic, and so should be able to help her.")')
    else:
        print("She sighs sadly and doesn't comment further.")

def janalquestwin(pc, npc):
    print("Janal rushes upstairs, and after a few minutes comes back down to talk to you. She thanks you profusely, and gives you almost thirty gold, saying it's the least she can do after what you've done.")
    pc.gold += 27
    print("You gain 27 gold. You now have a total of "+str(pc.gold)+" gold.")
    npc.addtalk(2, "Ask how Wrynn has been doing", 'print("She says she\'s been doing great since you healed her, and that they\'re hopeful that whatever was wrong was completely fixed by your magic.")')

def wardentelltoletgo(pc, npc):
    print('"No," she says. "Keeping the prisoners imprisoned is my job, and whatever issues I might have with the new management\'s treatment of them, I\'m not going to abandon my post just because some teenager who shouldn\'t even be in here told me to."')
    npc.addtalk(2, 'Offer her gold in exchange for letting the prisoner go', 'interactions.bribewarden(self.pc, self.npc)')

def bribewarden(pc, npc):
    print('"Do you just not understand the concept of loyalty? I serve the needs of Nephosopolis proudly, and no bribe is going to make me turn against that."')
    npc.deltalk(3)
    npc.addtalk(2, 'Try to convince her to join you against Melthar', 'print("She shakes her head and interrupts you almost as soon as you start. \\\"I really don\\\'t care what new angle you\\\'re taking to get me to betray my job this time. It\\\'s not going to work.\\\"")')

def wardenjoinspc(pc, npc, interaction):
    print("You ask her to join you against Melthar. She says no. You ask her why. She says she's loyal to the city, even if she might disagree with some of the leadership's choices. You ask her if she really thinks the city will survive much longer under Melthar's rule. This time, your question gives her pause.")
    print("\nAfter a moment, she agrees that it probably won't. She still refuses to act directly against Melthar, but agrees that it might be for the best if she were to 'accidentally' drop her keys and let slip that Melthar has been going to strangely great lengths to hide something underneath her throne room. Then she places her keys on her desk for you to pick up and leaves. Cell Door Keys acquired.")
    npc.drop('cell door keys')
    pc.pickup('cell door keys')
    npc.flags['melthar'].flags['wardenturned'] = True
    interaction.running = False
    npc.location.contents.remove(npc)

def terrifiedguardconvo(npc):
    print("He tells you that, a few days ago, Melthar started systematically replacing all non-essential palace guards with shadows and taking them away to who-knows-where. The only reason he wasn't replaced was because he works in the palace's intelligence branch, and the shadows aren't smart enough to replace him at that. But he thinks it's only a matter of time before she either figures something out or gives up on the branch altogether, and then he'll be taken too. But if he deserts then he'll just be killed even sooner.")
    npc.addtalk(2, "Ask what's happening to the other guards", 'print("He doesn\\\'t know for sure; they\\\'re just taken down to somewhere below the dungeons and never seen again.")')
    npc.addtalk(3, "Ask for his help overthrowing Melthar", 'interactions.gainpasskey(self.pc, self.npc, self.npc.flags["shadowguards"])')

def gainpasskey(pc, npc, shadowguards):
    print('He nods. "There\'s no way I\'m going to fight her or any of her minions myself," he says, "but take this." He hands you what looks like a black keycard. "As long as you\'re carrying this, the shadows will think you\'re one of us, and will hopefully let you around unhindered. You\'ll be on your own once you get into the throne room, but this will hopefully help you get there."')
    npc.drop('shadow passkey')
    pc.pickup('shadow passkey')
    npc.deltalk(3)
    if 'throne room key' in shadowguards.inventory:
        shadowguards.addtalk(4, 'Show them your passkey', 'interactions.shadowguardpasskey(self.pc, self.npc, self)')

def shadowguardbluffsuccess(npc, interaction):
    print('You walk up to them and, with your best demanding voice, tell them, "I was supposed to see the queen an hour ago. Let me through."\n\nThey talk amongst themselves for a moment, generally nodding, and one of them opens the door and waves you through. New exit opened in the following direction: North.')
    npc.unlock('massive door')
    interaction.running = False
    npc.deltalk(2)
    npc.deltalk(3)
    if 4 in npc.talktree.descriptions:
        npc.deltalk(4)

def shadowguardrecruit(npc):
    print("You attempt to recruit the guards. They appear extremely tempted, even before you've started really arguing for it. However, they never progress beyond that point; while they always look tempted to defect, they keep eventually concluding that they're going to serve Melthar, even if they agree with all your points. Neither you nor they are sure why that would be.")
    npc.addtalk(2, 'Try to bluff your way past them', 'interactions.shadowguardblufffailure(self.npc)')
    npc.addtalk(3, 'Try to convince them to join you against Melthar', 'print("You continue arguing, and they continue agreeing with your points but refusing to defect. You wonder if there\\\'s some sort of mind control at play here...")')

def shadowguardblufffailure(npc):
    print('You walk up to them and, with your best demanding voice, tell them, "I was supposed to see the queen an hour ago. Let me through."\n\nThey look unconvinced, probably because of the protracted debate you just held with them trying to get them to defect against the very same queen you claim to be meeting. You\'ll need some sort of proof if you want them to let you past.')

def shadowguardpasskey(pc, npc, interaction):
    if 'shadow passkey' in pc.inventory:
        print('You show them your passkey and ask to be let in the throne room. They nod and open the door for you. New exit opened in the following direction: North.')
        npc.unlock('massive door')
        interaction.running = False
        npc.deltalk(2)
        npc.deltalk(3)
        if 4 in npc.talktree.descriptions:
            npc.deltalk(4)
    else:
        print('You attempt to show them your passkey, but it seems you\'ve lost it somewhere. The guards are understanding, and don\'t try to kick you out of the castle, but say they can\'t just let you in on the basis of a passkey you don\'t actually have.')

def meltharconvostart(npc, val, interaction):
    if val == 4:
        interaction.curr = interaction.base.contents[2]
        npc.addtalk(1, 'Back', 'self.curr, self.attackready = self.base, False')
        npc.deltalk(2)
        npc.deltalk(3)
        npc.deltalk(4)
        return None
    elif val == 1:
        print('\n"Destroying the city?" She shakes her head. "I\'m using the city as my testing ground, true, but it will be entirely intact when I finish with it."')
    elif val == 2:
        print('\nShe sighs. "Revenge? Really? I was hoping your reason would be a bit more substantial than that. I guess I overestimated you."')
    elif val == 3:
        print('\n"I don\'t know why shadows have such a bad reputation. They\'re admittedly not very intelligent, but they\'re some of the most loyal creatures a person could ever meet."')
    print('\n"Let me be completely clear about what I\'m doing. Once I perfect the shadow hybridization process, I will apply it to every resident of Nephosopolis. I will then use our city as a base of operations from which to take over and hybridize the rest of the world. Everyone will come out happy; I\'ll get to rule the world, everyone else will get to be ruled by me, and the shadows will finally, at least for as long as I live, emerge truly victorious over the light. Is that not a goal worth pursuing?"')
    npc.addtalk(1, 'Back', 'self.curr, self.attackready = self.base, False')
    npc.addtalk(2, 'Try to convince her to give up her plan', 'interactions.melthardiplomacy(self.pc, self.npc)')
    npc.addtalk(3, 'Try to get her to keep monologuing while you look for her power item', 'interactions.meltharmonologue(self.pc, self.npc)')
    npc.deltalk(4)

def melthardiplomacy(pc, npc):
    print("\nYou try your best to argue her into stopping her plan. You point out that everybody will hate her. She says they won't once they've been hybridized. You argue that life will be empty for her if everyone just follows her orders. She says she knows herself better than you know her, thank you very much. You argue that the world is really huge, and there's no way she'll actually conquer it all. She says you're underestimating her.")
    print("\nIt doesn't seem like there's anything you can do to convince her. Looks like you'll have to find some other way.")
    npc.addtalk(2, 'Try to convince her to give up her plan', 'print("\\nYou argue some more that her plan is doomed. She\\\'s not any more convinced this time around.")')

def meltharmonologue(pc, npc):
    if npc.flags['wardenturned']:
        print('\nYou ask her about random details of her plan, since she\'s so happy to talk about it, and while she monologues you look for where she might have hidden her power item. Remembering what the warden told you about Melthar hiding something under her throne room, you look for some sort of trapdoor or loose floorboard or the like.')
        print('\nAfter a moment, you see a trapdoor, and begin nonchalantly moving towards it. You\'re almost there before Melthar realizes what you\'re doing, and by then you\'re close enough to wrench the trapdoor open and spot a book placed just under it, which you immediately tear in half.')
        print('\nMelthar screams and seems to be trying to perform some kind of magical attack against you, but nothing happens. As you watch, the sphere of darkness in the middle of the room begins to fade, and the throne room suddenly seems much brighter. Melthar looks outraged, though...')
        npc.attack = npcpunch
        npc.location.contents.remove(npc.flags['shadowlocus'])
        npc.hostile = True
        npc.addtalk(3, 'Tell her to surrender', 'interactions.meltharsurrender(self.pc, self.npc, self)')
    else:
        print('\nYou ask her about random details of her plan, since she\'s so happy to talk about it, and while she monologues you look for where she might have hidden her power item. This goes on for almost five minutes before she gets suspicious, but you don\'t find anything viable, and she\'s stopped talking and is now just looking at you strangely.')
        npc.deltalk(3)

def meltharsurrender(pc, npc, interaction):
    print('\nYou tell her to surrender. After a moment of staring at her fists and resolutely avoiding your gaze, Melthar finally sighs and lets her guard down. "Fine," she says. "Fine. You win. I can\'t do anything without my magic. I hope you eventually meet Talak and it pays you back for this, but trying to do it myself will just get me killed. Take me to prison or wherever you\'re planning to take me, I guess."')
    print('\nYou take her back to your own home, where you keep her imprisoned until a new government is in place to hold her, then turn her over to them. She is tried, and eventually sentenced to life in prison. Nephosopolis recovers surprisingly quickly from the damage Melthar did to it during her month of rule, and your life returns almost to normal (although you retain your magical abilities).')
    interaction.attackready = False
    interaction.running = False
    pcwin(pc)

#####################
#   Spell Effects   #
#####################

def housingflare(pc, npc): #Lets you use Flare to steal the key from the housing manager
    takekey = input('The housing manger is momentarily blinded. Do you want to try to steal the key before he recovers? Y/N\n>').lower()
    if takekey == 'y' or takekey == 'yes':
        print('You snatch the key from its hook while the manager is disoriented. He notices it missing a moment afterwards, and looks like he\'s barely resisting the urge to lunge at you and grab it back; you should probably avoid him from now on. Housing Manager is now hostile. Windowless Building Key acquired.', end='')
        npc.drop('windowless building key')
        pc.pickup('windowless building key')
        npc.deltalk(2)
        npc.hostile = True
    else:
        print('After a moment, the shopkeeper recovers. He glares at you, but doesn\'t say anything.', end='')

def shadowflare(pc, npc): #Makes Flare damage shadows
    npc.health -= 20
    print('The shadow recoils from the sudden brightness. '+npc.name+' has '+str(npc.health)+' health remaining.', end='')

def shadowtunnelflare(): #Prints a response to casting Flare in the Shadow Tunnel
    print('Your flare wards the shadows off for a moment, but only a moment. Within seconds they are once again closing in on you.', end='')

#################
#   NPC Loops   #
#################

def wrynnhealcheck(npc): #Checks if Wrynn has been healed, and updates her accordingly
    if npc.flags['healed'] == True:
        return None
    elif npc.health > 40:
        print("\nWrynn looks much better now. You don't know if you've cured her completely, but you've at least helped her as far as you're capable. You should go downstairs and tell Janal.")
        npc.describe("She's looking much better now. Good job!", 'interaction')
        npc.describe("You see Wrynn. She's sitting up and reading.", 'short')
        npc.describe("An old woman, sitting and reading a book whose title you can't make out.")
        npc.addtalk(2, "Ask how she feels now", 'print("She says she feels much better, and thanks you for the healing.")')
        npc.flags['wife'].addtalk(2, "Tell her you've healed Wrynn", "interactions.janalquestwin(self.pc, self.npc)")
        npc.flags['healed'] = True
    elif npc.flags['partlyhealed'] == True:
        return None
    elif npc.health > 30:
        print("\nWrynn looks a bit better. She still looks fragile, but her breathing becomes stronger and she no longer looks like she's on the brink of death. You're pretty sure you can do more for her, though.")
        npc.describe('She looks better than she did before, but still not what you would call \'healthy\'.', 'interaction')
        npc.flags['partlyhealed'] = True

def housingmanagerhpcheck(pc, npc): #Checks if the housing manager is almost dead and if he wants to surrender
    if npc.health <= 10 and npc.hostile:
        if 'windowless building key' in npc.inventory:
            print("\nThe housing manger surrenders in terror, and tells you that you can take whatever you want. Just don't kill him, he begs you. You take the key to the abandoned building, but it doesn\'t feel like a victory. Housing Manger is no longer hostile. Windowless Building Key acquired.")
            npc.drop('windowless building key')
            pc.pickup('windowless building key')
            npc.hostile = False
        else:
            print('\n"You\'ve already got the key!" the manager yells. "What more could you possibly want?!"')

def shadowaccumulatordeath(pc, npc, interaction): #Converts the Shadow Accumulator into the Cloud of Tools without ending the interaction
    print('\nThe accumulator shatters into dozens of pieces, and the shadows stop accumulating where it stood, cutting off the stream down the tunnel. For a moment you think that\'s the end of it. But then you hear a rumbling, and an animated cloud of lab tools begins to attack you. Apparently breaking the accumulator didn\'t disperse the magic that was powering it...')
    npc.location.exits['north'].flags['pacified'] = True
    npc.location.exits['north'].connect(npc.location.exits['north'].flags['destination'], 'north')
    npc.location.exits['north'].connect(npc.location, 'south')
    npc.location.exits['north'].describe('You enter the tunnel the shadows were being sent down. It runs a very long way north.', 'short')
    npc.location.exits['north'].describe('A very long tunnel through the underclouds, running to the north. Surprisingly clear of shadows, now that the accumulator is destroyed. You wonder where they all went.')
    npc.location.describe('You enter the room which previously contained the shadow accumulator.', 'short')
    npc.name = 'Cloud of Tools'
    npc.attack = toolwhirlwind
    npc.health = 60
    npc.describe('A spinning cloud of floating lab equipment. You see some hammers, some pipe segments, a saw... You\'d better deal with it quickly, before it tears you to shreds.')
    interaction.base.contents[1].remove(2)
    interaction.base.add(5, 'Leave', 'print("You try to run away, but the cloud of tools stays stubbornly close to you. Looks like you\\\'ll have to fight your way out of this one.")')
    interaction.npcdeath = 'print(interactions.npcdeath(self.npc))'
    interaction.curr = interaction.base
    interaction.running = True
    interaction.attackready = False
    print('\nYou are no longer interacting with Shadow Accumulator.')
    print('\nYou are now interacting with Cloud of Tools. It looks hostile.')

def melthardeath(pc, npc): #Player wins when Melthar dies
    npc.die()
    print('\nFinally, Melthar dies. Your work here is done, and you return home. It doesn\'t take too long for the old government to reconsolidate now that Melthar is out of the way, and soon they\'re back in place, systematically reversing all the damage she\'s done. It takes the city a surprisingly short time to recover from her rule, and for you to return to an almost-normal life (although you still have your magic).')
    pcwin(pc)

##################
#   Room Loops   #
##################

def shadowtunnelscary(pc, room): #If there's still a stream of shadows flowing into the tunnel, has them menace and eventually kill the PC
    if not room.flags['pacified']:
        if room.flags['warning3']:
            print('\nA shadow suddenly speeds toward you from behind, and as you turn to fight it, five more lunge at you from all around. You attempt to ward them off with a flare, but there are too many, moving too quickly, and you\'re surrounded. You are devoured by the shadows.')
            pc.die()
        elif room.flags['warning2']:
            print('\nEven with the occasional flare to drive them off, the shadows seem closer than before. You should probably get out of here before they\'re on top of you.')
            room.flags['warning3'] = True
        elif room.flags['warning1']:
            print('\nAs you continue down the tunnel, the shadows seem to be surrounding you. You\'re not sure you should be in here...')
            room.flags['warning2'] = True
        else: #not room.flags['warning1']
            print('\nAs you enter the tunnel, you are accosted by a hostile living shadow.')
            room.flags['warning1'] = True
            room.flags['shadow'].move('up')
            commands.interact('shadow')

def dungeondoorcheck(door, prisoner, pc): #Checks for when the PC has opened the dungeon's internal door
    if door.location.flags['dooropened'] == False and not door in door.location.contents and prisoner in door.location.contents:
        door.location.flags['dooropened'] = True
        print("The prisoner rushes outside the door as soon as you open it, as if she's afraid you'll close it if she waits too long. A moment after she's out, she turns to you.")
        print('\n"Thanks," she says. "I thought I was done for there. Is the way you came in safe for me to leave by?"')
        print("\nYou confirm it's safe and summarize the path, and she nods and begins to climb downstairs. Before fully disappearing, though, she pauses for a moment and hands you a health potion, telling you that she snuck it from a storeroom upstairs on the way in, and that you probably need it more than her if you're planning on staying here.")
        prisoner.drop('health potion')
        pc.pickup('health potion')
        prisoner.location.contents.remove(prisoner)

def palacerealization(room): #The PC realizing they're in the palace
    if room.flags['realized'] == False:
        print("\nWait a minute... you recognize this architecture. Did the tunnel from Melthar's lair lead you straight to the palace? That explains some things about how she took over.")
        room.flags['realized'] = True

def barracksentry(room): #The barracks' guard making his opinions clear
    if room.flags['entered'] == False:
        print('\n"I surrender!" yells the guard as soon as you walk in.')
        room.flags['entered'] = True

def storeroomshadows(pc, room): #Random encounters with shadows in the storeroom
    if 'shadow passkey' in pc.inventory:
        if not room.flags['usedpasskey']:
            print('\nThe patrolling shadows ignore you thanks to your passkey.')
            room.flags['usedpasskey'] = True
    elif room.flags['firstentry']:
        print('\nShadows patrol this room. Their coverage seems inconsistent, but you doubt it will take too long for one of them to run into you.')
        room.flags['firstentry'] = False
    elif not room.flags['roomcleared']:
        encounterchance = len(room.flags['shadows'])
        if random.randint(0, 9) < encounterchance:
            room.flags['shadows'][0].move('down')
            del room.flags['shadows'][0]
            print('\nA shadow notices you and attacks.')
            commands.interact('shadow')
        elif encounterchance > 0:
            print('\nShadows patrol the room, but none notice you.')
        else:
            print('\nYou seem to have dispersed the last of the patrolling shadows.')
            room.flags['roomcleared'] = True

def throneroomentry(pc, npc): #Begins the final boss encounter
    if not pc.location.flags['entered']:
        print("You look around the throne room as you enter, and find Queen Melthar herself, standing in front of a huge sphere of darkness floating in midair, clearly waiting for you.")
        print('\n"Ah, there you are," she says. "I was wondering when you were going to show up. I see you\'ve met my new guards outside. They\'re not perfected just yet, but at the rate my research is going, it will only be a few more days before they\'re both as smart as my human guards and as loyal as my shadows. Then, finally, I\'ll be able to move on with my plan. I suppose it might be a bit longer now that you\'ve broken my lab, but no matter. I\'m sure you were doing what you thought was right."')
        print('\n"Talak says it\'s a waste of time and I shouldn\'t bother, but I am curious, so I\'m going to give you a chance to explain yourself before doing anything drastic. What, exactly, do you think you\'re going to accomplish by overthrowing me?"')
        commands.interact(npc.name.lower(), 1)
        pc.location.flags['entered'] = True

#############
#   Debug   #
#############

def weponshoot(target):
    target.health -= 999999
    return 'shot the thing with wepon'