import textwrap
import panda3d.core


cardCollisionMask = panda3d.core.BitMask32.bit(31)


def buildCard(self, card, parent):
    cardBase = parent.attachNewNode(card.name)

    cm = panda3d.core.CardMaker(card.name)

    cardFrame = cardBase.attachNewNode(cm.generate())
    tex = loader.loadTexture('ul_frame_alt.png')
    cardFrame.setTexture(tex)
    cardFrame.setScale(1, 1, 509 / 364)
    cardFrame.setTransparency(True)
    cardFrame.setName('frame')

    cardImage = cardBase.attachNewNode(cm.generate())
    try:
        tex = loader.loadTexture(card.imagePath)
    except IOError:
        tex = loader.loadTexture('base_icons/missing.png')
    cardImage.setTexture(tex)
    cardImage.setScale(0.7)
    cardImage.setPos(0.15, -0.05, 0.5)
    cardImage.setName('image')

    name = panda3d.core.TextNode('name')
    name.setAlign(panda3d.core.TextNode.ARight)
    name.setText(card.name)
    textNodePath = cardBase.attachNewNode(name)
    textNodePath.setScale(0.08)
    textNodePath.setPos(0.92, -0.05, 1.275)

    cost = panda3d.core.TextNode('cost')
    cost.setText(str(card.cost))
    textNodePath = cardBase.attachNewNode(cost)
    textNodePath.setScale(0.1)
    textNodePath.setPos(0.08, -0.05, 1.275)
    card.costNode = cost

    rank = panda3d.core.TextNode('rank')
    rank.setText(str(card.rank))
    textNodePath = cardBase.attachNewNode(rank)
    textNodePath.setScale(0.1)
    textNodePath.setPos(0.08, -0.05, 1.125)
    card.rankNode = rank

    desc = panda3d.core.TextNode('desc')
    desc.setText(textwrap.fill(card.desc, width=25))
    textNodePath = cardBase.attachNewNode(desc)
    textNodePath.setScale(0.07)
    textNodePath.setPos(0.09, -0.05, 0.4)

    counter = panda3d.core.TextNode('counter')
    textNodePath = cardBase.attachNewNode(counter)
    textNodePath.setScale(0.4)
    textNodePath.setPos(0.7, -0.05, 0.1)
    card.counterNode = counter

    if hasattr(card, 'counter'):
        counter.setText(str(card.counter))

    cardBase.setPythonTag('card', card)
    card.pandaNode = cardBase

    cardBase.setCollideMask(cardCollisionMask)

    return cardBase


def buildBlankCard(self, card, parent):
    cardBase = parent.attachNewNode('mysterious card')
    cm = panda3d.core.CardMaker('mysterious card')
    cardFrame = cardBase.attachNewNode(cm.generate())
    tex = loader.loadTexture('ul_frame_alt.png')
    cardFrame.setTexture(tex)
    cardFrame.setScale(1, 1, 509 / 364)
    cardFrame.setTransparency(True)
    cardFrame.setName('frame')
    cardBase.setPythonTag('card', card)
    cardBase.setCollideMask(cardCollisionMask)
    return cardBase


def updateCard(card):
    card.costNode.setText(str(card.cost))
    card.rankNode.setText(str(card.rank))
    if hasattr(card, 'counter'):
        card.counterNode.setText(str(card.counter))
