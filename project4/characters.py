#This module contains all generation code for things which inherit from Character

import engine
import interactions

###########
#   PCs   #
###########

def raelina(location):
    raelina = engine.PC('Raelina', location, 100, ['Flare', 'Heal'], ['flare', 'heal'])
    raelina.gold = 10
    raelina.casttree = engine.Node({1:'Back', 2:'Flare', 3:'Heal self', 4:'Heal NPC'}, {1:'self.curr, self.attackready = self.base, False', 2:'print(interactions.flare(self.npc))', 3:'print(interactions.heal(self.pc))', 4:'print(interactions.heal(self.npc))'})
    raelina.describe("Your name is Raelina.") #Fancify description
    return raelina

def sarille(location):
    sarille = engine.PC('Sarille', location, 100, ['Read', 'Scry'], ['read', 'scry'])
    sarille.gold = 54

def lanise(location):
    lanise = engine.PC('Lanise', location, 100, ['Disintegrate', 'Shield'], ['disintegrate', 'shield'])
    lanise.describe("Your name is Lanise.") #Fancify description
    return lanise

############
#   NPCs   #
############

def beggar(location):
    beggar = engine.NPC('Beggar', location, 50, interactions.npcpunch, 'He')
    beggar.describe('You see a weary-looking man with a sign asking for money.', 'short')
    beggar.describe('Between the sediment accumulated on his skin and the worn-down look of his clothes, this man has clearly been on the streets for a while.')
    beggar.describe('As you speak with him, he periodically glances at your coin purse, clearly hoping for some money.', 'interaction')
    beggar.addtalk(2, 'Ask about the rumors', 'print("He tells you that there have been occasional sightings of unnaturally-moving shadows in the alley to the west at night, especially around one particular house which has, as far as anyone knows, been abandoned for months. The door is locked, though, so nobody has been able to investigate in detail.")')
    beggar.addtalk(3, 'Give him two gold', 'interactions.helpbeggar(self.pc, self.npc)')
    return beggar

def housingmanager(location):
    housingmanager = engine.NPC('Housing Manager', location, 50, interactions.npcpunch, 'He')
    housingmanager.describe('You see a man in an official housing office uniform.', 'short')
    housingmanager.describe('A short, balding man, wearing a shirt and hat signifying that he works for the housing office. He doesn\'t seem very happy to be here.')
    housingmanager.describe('Although he\'s trying to mask it, the housing manager is exuding a tangible mood of resignation.', 'interaction')
    housingmanager.addtalk(2, 'Ask to buy the key to the windowless building', 'interactions.askforkey(self.pc, self.npc)')
    housingmanager.spellresponse('flare', 'housingflare(commands.scripts.currprotag, item)')
    housingmanager.setinteractloop('interactions.housingmanagerhpcheck(self.pc, self.npc)')
    return housingmanager

def shopkeeper(location):
    shopkeeper = engine.NPC('Shopkeeper', location, 50, interactions.npcpunch, 'He')
    shopkeeper.describe('You see the shopkeeper.', 'short')
    shopkeeper.describe('Probably the youngest shopkeeper you\'ve seen, barely out of his teens. He seems very eager about his work.')
    shopkeeper.describe('His eyes seem to try to follow yours at every opportunity; whenever you look at an item, he looks at the same item a moment later, as if hoping to divine something about you from what you look at.', 'interaction')
    shopkeeper.addtalk(2, 'Ask to sell something', 'print("He shakes his head before you\'ve even finished your request. \\\"Sorry\\\", he says, \\\"but I\\\'m already overstocked as it is. Feel free to buy something to help take the load off, though.\\\"")')
    shopkeeper.addtalk(3, 'Ask what he has for sale', 'interactions.findwand(self.pc, self.npc)')
    return shopkeeper

def janal(location):
    janal = engine.NPC('Janal', location, 50, interactions.npcpunch, 'She', {'wife':None})
    janal.describe('You see an old and tired-looking woman.', 'short')
    janal.describe('She has grey hair, a wrinkled face, and a generally tired demeanor, but still appears alert, examining you as much as you\'re examining her.')
    janal.addtalk(2, 'Ask about the sign on her door', 'interactions.janalqueststart(self.pc, self.npc)')
    return janal

def wrynn(location):
    wrynn = engine.NPC('Wrynn', location, 30, interactions.npcflail, 'She', {'wife':None, 'partlyhealed':False, 'healed':False})
    wrynn.describe('You see an old woman who looks like she\'s barely conscious.', 'short')
    wrynn.describe('She\'s lying down in bed, breathing worryingly slowly, and her eyes are closed, although a perking of her ears suggests that she\'s still tracking your presence.')
    wrynn.describe('She looks days off from death.', 'interaction')
    wrynn.setinteractloop('interactions.wrynnhealcheck(self.npc)')
    return wrynn

def shadowaccumulator(location):
    shadowaccumulator = engine.NPC('Shadow Accumulator', location, 40, interactions.nonattack, 'It')
    shadowaccumulator.describe('You see a large shadow-filled orb.', 'short')
    shadowaccumulator.describe('A very large orb occupying the center of the room. Every few seconds, it lets out a pulse, and the shadows within it seem to deepen slightly. As you watch it for a few minutes, the shadows become deeper and deeper, and eventually are pulled out of the orb by a tube, running through the tube into the tunnel leading to the north. It has a user interface on one side, which you ought to be able to access.')
    shadowaccumulator.describe('Shadows continue to accumulate within the orb as you interact with it.', 'interaction')
    shadowaccumulator.addnpcdeathoverride('interactions.shadowaccumulatordeath(self.pc, self.npc, self)')
    shadowaccumulator.addtalk(2, 'Check the system diagnostics', 'print("This device is apparently collecting every bit of decaying magic from Melthar\\\'s shadow army and recoalescing it into new shadow monsters. As long as it runs, her army will be effectively endless. You wonder how easy it would be to destroy...")')
    return shadowaccumulator

def shadow(location):
    shadow = engine.NPC('Shadow', location, 70, interactions.shadowattack, 'It', {}, True)
    shadow.describe('You see a patch of darkness moving of its own volution.', 'short')
    shadow.describe('A patch of darkness which remains stubbornly resistant to any perturbations to its surrounding light, shifting somewhat even without changes in light and not being eliminated as much as it should when light does touch it.')
    shadow.spellresponse('flare', 'shadowflare(commands.scripts.currprotag, item)')
    shadow.setoverride('5', 'Leave', 'print("You try to run away, but the shadow stays stubbornly engaged with you. You don\\\'t think you\\\'ll be able to get away safely before dispersing it.")')
    return shadow

def prisoner(location):
    prisoner = engine.NPC('Prisoner', location, 50, interactions.npcpunch, 'She')
    prisoner.describe('You see a prisoner in the cells.', 'short')
    prisoner.describe('A girl barely older than you, likely still in her teens. She looks hopefully at you through the bars of her cell.')
    prisoner.describe('She looks intensely focused on you, as if you\'re the most interesting thing she\'s seen all day. Maybe you are.', 'interaction')
    prisoner.addtalk(2, 'Ask how she got put in here', 'print("She tells you that she was thrown in here after trying to sneak past the guards at one of the blockaded districts in order to visit her sick grandmother.\\n\\nShe also tells you that there used to be more prisoners here, some for even more ridiculous reasons, but that they\\\'ve been systematically taken away and now it\\\'s only her left. She doesn\\\'t know where they were being taken, but doubts it\\\'s anywhere good. She asks you to get her out before the same thing happens to her.")')
    prisoner.addtalk(3, 'Ask where you can find the key to her cell', 'print("She says that the prison\\\'s warden keeps the keys on her at all times, and that last time she saw her go by it was into her office to the east, so she expects you can find her and her keys there.")')
    return prisoner

def warden(location):
    warden = engine.NPC('Warden', location, 70, interactions.npcsword, 'She', {'melthar':None})
    warden.describe('You see the prison\'s warden.', 'short')
    warden.describe('A serious-looking woman in light armor, with a key ring and a sword attached to her belt.')
    warden.describe('She looks at you disapprovingly, and clearly recognizes that you shouldn\'t be here, but doesn\'t seem to be trying to raise the alarm on you, either.')
    warden.addtalk(2, 'Tell her to let the prisoner go', 'interactions.wardentelltoletgo(self.pc, self.npc)')
    warden.addtalk(3, 'Try to convince her to join you against Melthar', 'interactions.wardenjoinspc(self.pc, self.npc, self)')
    return warden

def guard(location):
    guard = engine.NPC('Terrified Guard', location, 60, interactions.npcsword, 'He', {'shadowguards':None})
    guard.describe('You see a terrified-looking guard.', 'short')
    guard.describe("One of Melthar's guards. Currently curled into a ball on one of the room's many beds, looking around nervously.")
    guard.describe("He seems, if anything, calmer interacting with you than he did when you came in.", "interaction")
    guard.addtalk(2, 'Ask what has him so afraid', 'interactions.terrifiedguardconvo(self.npc)')
    return guard

def throneroomguards(location):
    throneroomguards = engine.NPC('Strange-Looking Guards', location, 90, interactions.shadowguardsatt, 'Strange-Looking Guards') #No 'they' pronoun because it would interact gramatically incorrectly with the combat system
    throneroomguards.describe('You see a strange-looking group of guards.', 'short')
    throneroomguards.describe('You see a group of guards around whom light flows strangely, seeming to land on them far less than it does on their surroundings.')
    throneroomguards.describe('The more you look at these guards, the more the behavior of the light around them reminds you of Melthar\'s shadows.\n\nThey look very well-prepared for a fight, but also unfocused. You wonder if you can bluff your way past them.', 'interaction')
    throneroomguards.addtalk(2, 'Try to bluff your way past them', 'interactions.shadowguardbluffsuccess(self.npc, self)')
    throneroomguards.addtalk(3, 'Try to convince them to join you against Melthar', 'interactions.shadowguardrecruit(self.npc)')
    throneroomguards.spellresponse('flare', 'print("The guards wince slightly at the light, but don\\\'t seem affected by it to the same degree a shadow would be.")')
    return throneroomguards

def meltharnpc(location):
    melthar = engine.NPC('Melthar', location, 100, interactions.meltharcombat, 'She', {'shadowlocus':None, 'wardenturned':False})
    melthar.describe('You see Queen Melthar.', 'short')
    melthar.describe('Melthar, self-declared queen of Nephosopolis. Her reign has been marked by terrible rulership and dramatic magic-use to enforce it; but, if you have your way, it will end today.')
    melthar.addtalk(1, "You need to stop her because she's destroying the city.", 'interactions.meltharconvostart(self.npc, 1, self)')
    melthar.addtalk(2, "You're here to avenge everyone she murdered in her takeover.", 'interactions.meltharconvostart(self.npc, 2, self)')
    melthar.addtalk(3, "You don't know her exact plan, but no plan involving an army of evil shadows could possibly be good.", 'interactions.meltharconvostart(self.npc, 3, self)')
    melthar.addtalk(4, "You don't need to justify yourself to her. Just attack.", 'interactions.meltharconvostart(self.npc, 4, self)')
    melthar.setoverride('5', 'Leave', 'print("\\\"Where do you think you\\\'re going?\\\" Melthar asks. You notice that the door has been closed behind you at some point. \\\"We\\\'re not done here yet.\\\"")')
    melthar.addnpcdeathoverride('interactions.melthardeath(self.pc, self.npc)')
    return melthar