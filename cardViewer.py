import argparse
import importlib

import panda3d.core
import direct.showbase.ShowBase
from direct.task import Task

import cardBuilder

panda3d.core.loadPrcFileData('', 'model-path assets')

#parser = argparse.ArgumentParser()
#parser.add_argument('-f', type=str, default='ul_core.factions.templars')
#parser.add_argument('-c', type=str, default='Equus')
#args = parser.parse_args()

#mod = importlib.import_module(args.f)
#card = getattr(mod, args.c)()

import ul_core.factions.templars as templars

base = direct.showbase.ShowBase.ShowBase()
base.disableMouse()

class FakePlayer:
    iconPath = 'templar_icons'  # Hack to make icon paths work
    manaCap = 0  # Equus rank hack

card = templars.equus()
card.owner = FakePlayer()
node = base.render.attachNewNode('card_root')
node.setPos(0, 5, 0)
cardNode = cardBuilder.buildCard(None, card, node)
cardNode.setPos(-0.5, 0, -0.5)

def mouseRotate(task):
    if base.mouseWatcherNode.hasMouse():
        x = base.mouseWatcherNode.getMouseX() * 100
        node.setHpr(x, 0, 0)

    return Task.cont

base.addTask(mouseRotate)

base.run()
