import argparse
import importlib

import panda3d.core
import direct.showbase.ShowBase
from direct.task import Task

import cardBuilder

panda3d.core.loadPrcFileData('', 'model-path assets')

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default='templars')
parser.add_argument('-c', type=str, default='equus')
args = parser.parse_args()

mod = importlib.import_module('ul_core.factions.' + args.f)
card = getattr(mod, args.c)()

base = direct.showbase.ShowBase.ShowBase()
base.disableMouse()

class FakePlayer:
    iconPath = 'templar_icons'  # Hack to make icon paths work
    manaCap = 0  # Equus rank hack

card.owner = FakePlayer()
node = base.render.attachNewNode('card_root')
node.setPos(0, 5, 0)
cardNode = cardBuilder.buildCard(None, card, node)
cardNode.setPos(-0.5, 0, -0.5)

class MouseRotator:
    def __init__(self):
        self.held = False
        base.addTask(self.mouseRotate)
        base.accept('mouse1', self.on_mouse1)
        base.accept('mouse1-up', self.on_mouse1_up)

    def mouseRotate(self, task):
        if base.mouseWatcherNode.hasMouse() and self.held:
            x = base.mouseWatcherNode.getMouseX() * 100
            node.setHpr(x, 0, 0)

        return Task.cont

    def on_mouse1(self):
        self.held = True

    def on_mouse1_up(self):
        self.held = False


MouseRotator()
base.run()
