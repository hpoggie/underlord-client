import argparse
import importlib

import panda3d.core
import direct.showbase.ShowBase
from direct.task import Task

import cardBuilder

import ul_core.factions
from ul_core.core.card import Card

import hud.hud

panda3d.core.loadPrcFileData('', 'model-path assets')

parser = argparse.ArgumentParser()
parser.add_argument('-c', type=str, default='equus')
args = parser.parse_args()

try:
    card = ul_core.factions.allCards[args.c]()
except KeyError:
    card = Card(name='mysterious card', cardId=-1)

base = direct.showbase.ShowBase.ShowBase()
base.disableMouse()
base.fonts = hud.hud.Fonts()

class FakePlayer:
    def __init__(self):
        self.manaCap = 0  # Equus rank hack

card.owner = FakePlayer()
node = base.render.attachNewNode('card_root')
node.setPos(0, 5, 0)
if hasattr(card, 'cardId') and card.cardId < 0:
    cardNode = cardBuilder.buildBlankCard(card, node)
else:
    cardNode = cardBuilder.buildCard(card, node)

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
