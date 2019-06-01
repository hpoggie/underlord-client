import textwrap
import panda3d.core


cardCollisionMask = panda3d.core.BitMask32.bit(31)


def makeCardFrame(cardBase):
    cardFrame = loader.loadModel('card.bam')
    cardFrame.reparentTo(cardBase)
    tex = loader.loadTexture('ul_frame_alt.png')
    cardFrame.setTexture(tex)
    cardFrame.setPosHprScale(0, 0, 0, 0, 90, 0, 0.075, 0.075, 0.05)
    cardFrame.setTransparency(True)
    cardFrame.setName('frame')
    return cardFrame


def buildCard(card, parent):
    cardBase = parent.attachNewNode(card.name)

    cm = panda3d.core.CardMaker(card.name)

    cardFrame = makeCardFrame(cardBase)

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
    nameNodePath = cardBase.attachNewNode(name)
    nameNodePath.setScale(0.08)
    nameNodePath.setPos(0.92, -0.05, 1.275)

    cost = panda3d.core.TextNode('cost')
    cost.setText(str(card.cost))
    costNodePath = cardBase.attachNewNode(cost)
    costNodePath.setScale(0.1)
    costNodePath.setPos(0.08, -0.05, 1.275)
    card.costNode = cost

    rank = panda3d.core.TextNode('rank')
    rank.setText(str(card.rank))
    rankNodePath = cardBase.attachNewNode(rank)
    rankNodePath.setScale(0.1)
    rankNodePath.setPos(0.08, -0.05, 1.125)
    card.rankNode = rank

    desc = panda3d.core.TextNode('desc')
    desc.setText(textwrap.fill(card.desc, width=25))
    descNodePath = cardBase.attachNewNode(desc)
    descNodePath.setScale(0.07)
    descNodePath.setPos(0.09, -0.05, 0.4)

    counter = panda3d.core.TextNode('counter')
    counterNodePath = cardBase.attachNewNode(counter)
    counterNodePath.setScale(0.4)
    counterNodePath.setPos(0.7, -0.05, 0.1)
    card.counterNode = counter

    for node in (cardImage, costNodePath, rankNodePath,
                 descNodePath, counterNodePath, nameNodePath):
        node.setPos(node.getX() - 0.5, node.getY(), node.getZ() - 0.7)

    for txt in (name, cost, rank, counter, desc):
        txt.setFont(base.fonts.bodyFont)

    if hasattr(card, 'counter'):
        counter.setText(str(card.counter))

    cardBase.setPythonTag('card', card)
    card.pandaNode = cardBase

    cardBase.setCollideMask(cardCollisionMask)

    # Mark the card as unlit so it's always readable
    cardBase.setLightOff(0)

    return cardBase


def buildBlankCard(card, parent):
    cardBase = parent.attachNewNode('mysterious card')
    cardFrame = makeCardFrame(cardBase)
    cardBase.setPythonTag('card', card)
    card.pandaNode = cardBase
    cardBase.setCollideMask(cardCollisionMask)
    return cardBase


def updateCard(card):
    card.costNode.setText(str(card.cost))
    card.rankNode.setText(str(card.rank))
    if hasattr(card, 'counter'):
        card.counterNode.setText(str(card.counter))
