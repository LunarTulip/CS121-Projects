#This module instantiates the world and then activates the text parser

import commands
import scripts

scripts.world = scripts.World()
scripts.world.start()

commands.parser()