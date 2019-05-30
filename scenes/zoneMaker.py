import panda3d.core
from panda3d.core import CardMaker, BitMask32
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

from .fanHand import fanHand
import animations
import cardBuilder

def hideCard(card):
    for ch in card.children:
        if ch.name != 'frame':
            ch.hide()


def showCard(card):
    for ch in card.children:
        if ch.name != 'frame':
            ch.show()


def cleanup(parent):
    for i in parent.children:
        c = i.getPythonTag('card')
        if c is None or c.cardId == -1:
            i.removeNode()


class ZoneMaker(DirectObject):
    def __init__(self, player,
                 scene, playerHand, enemyHand, playerBoard, enemyBoard,
                 playerFace, enemyFace, playerGraveyard, enemyGraveyard):
        self.player = player

        self.playerHand = playerHand
        self.enemyHand = enemyHand
        self.playerBoard = playerBoard
        self.enemyBoard = enemyBoard
        self.playerFace = playerFace
        self.enemyFace = enemyFace
        self.playerGraveyard = playerGraveyard
        self.enemyGraveyard = enemyGraveyard

        self.scene = scene

        base.playerIconPath = base.player.iconPath
        base.enemyIconPath = base.enemy.iconPath
        base.playerCardBack = base.player.cardBack
        base.enemyCardBack = base.enemy.cardBack

        for name in ['mulliganHand', 'orphan']:
            setattr(self, name, self.scene.attachNewNode(name))

        self.mulliganHand.reparentTo(base.camera)

        self.makePlayerFace()
        self.makeEnemyFace()

        # For showing a big version of a card on mouse over
        self.focusedCard = base.camera.attachNewNode('focused card')
        self.focusedCard.setPos(-0.5, 6, -0.3)

        for c in base.player.referenceDeck + base.enemy.referenceDeck:
            c.pandaNode = None

        self.lockMaker = CardMaker("lock icon")
        self.lockIcons = []

        base.taskMgr.add(self.resizeMulliganHandTask, 'ResizeMulliganHand')

    def addHandCard(self, card, tr, parent=None):
        if parent is None:
            parent = self.playerHand

        cardModel = self.loadCard(card)
        cardModel.setPosHpr(*tr)
        cardModel.setPythonTag('zone', base.player.hand)
        cardModel.reparentTo(parent)

    def makeMulliganHand(self):
        """
        Draw the player's hand for mulligan
        """
        cleanup(self.mulliganHand)

        posX = 0
        for c in base.player.hand:
            self.addHandCard(c, (posX, 0, 0, 0, 0, 0), self.mulliganHand)
            if c in base.toMulligan:
                hideCard(c.pandaNode)
            else:
                showCard(c.pandaNode)

            posX += 1.1

    def resizeMulliganHandTask(self, task):
        if self.player.hasMulliganed:
            return Task.done

        ratio = base.camLens.getAspectRatio()
        scale = max(ratio * 1.05, 1)
        self.mulliganHand.setPosHpr(
            -1.1 * (len(base.player.hand) - 1) / 2 * scale, 12, 0, 0, 0, 0)
        self.mulliganHand.setScale(scale, 1, scale)
        return Task.cont

    def makePlayerHand(self):
        """
        Redraw the player's hand.
        """
        self.mulliganHand.stash()
        # Destroy entire hand. This is slow and may need to be changed
        # cleanup(self.playerHand)
        for node in self.playerHand.children:
            node.removeNode()

        fan = fanHand(len(base.player.hand))
        for i, tr in enumerate(fan):
            self.addHandCard(base.player.hand[i], tr)

    def makeEnemyHand(self):
        for node in self.enemyHand.children:
            node.removeNode()

        def addEnemyHandCard(card, tr):
            if card.visible:
                cardModel = self.loadCard(card)
            else:
                cardModel = self.loadEnemyBlank(card)
            cardModel.setPosHpr(*tr)
            cardModel.setPythonTag('zone', base.enemy.hand)
            cardModel.reparentTo(self.enemyHand)

        fan = fanHand(len(base.enemy.hand))
        for i, tr in enumerate(fan):
            addEnemyHandCard(base.enemy.hand[i], tr)

    def makeLockIcon(self, card):
        lockModel = self.playerBoard.attachNewNode(self.lockMaker.generate())
        tex = loader.loadTexture("padlock.png")
        lockModel.setTexture(tex)
        lockModel.setPos(card, -0.5, 0, 1)
        lockModel.setHpr(base.camera, 0, 0, 0)
        self.lockIcons.append(lockModel)

    def makeBoard(self):
        """
        Show the player's faceups and facedowns
        """
        cleanup(self.playerBoard)

        width = 1.1 * (len(base.player.faceups) + len(base.player.facedowns))

        posX = 0.55 - width / 2

        def addFaceupCard(card):
            cardModel = self.loadCard(card)
            cardModel.reparentTo(self.playerBoard)
            cardModel.setPosHpr(posX, 0, 0, 0, 0, 0)
            cardModel.setPythonTag('zone', base.player.faceups)

        def addFdCard(card):
            cardModel = self.loadCard(card)
            hideCard(cardModel)
            cardModel.reparentTo(self.playerBoard)
            cardModel.setPosHpr(posX, 0, 0, 0, 0, 0)
            cardModel.setPythonTag('zone', base.player.facedowns)
            if not card.stale:
                self.makeLockIcon(cardModel)

        for c in base.player.faceups:
            addFaceupCard(c)
            posX += 1.1
        for c in base.player.facedowns:
            addFdCard(c)
            posX += 1.1

    def makeEnemyBoard(self):
        cleanup(self.enemyBoard)
        for n in self.enemyBoard.children:
            n.reparentTo(self.orphan)

        width = 1.1 * (len(base.enemy.faceups) + len(base.enemy.facedowns))

        posX = 0.55 - width / 2

        def addEnemyFdCard(card):
            if card.visible:
                cardModel = self.loadCard(card)
                hideCard(cardModel)
            else:
                cardModel = self.loadEnemyBlank(card)
            cardModel.reparentTo(self.enemyBoard)
            cardModel.setPos(posX, 0, 0)
            cardModel.setPythonTag('zone', base.enemy.facedowns)
            if not card.stale:
                self.makeLockIcon(cardModel)

        def addEnemyFaceupCard(card):
            cardModel = self.loadCard(card)
            cardModel.reparentTo(self.enemyBoard)
            cardModel.setPos(posX, 0, 0)
            cardModel.setPythonTag('zone', base.enemy.faceups)

        for c in base.enemy.faceups:
            addEnemyFaceupCard(c)
            posX += 1.1
        for c in base.enemy.facedowns:
            addEnemyFdCard(c)
            posX += 1.1

    def makePlayerGraveyard(self):
        # Show only the top card for now
        if len(base.player.graveyard) > 0:
            cleanup(self.playerGraveyard)
            c = self.loadCard(base.player.graveyard[-1])
            showCard(c)
            c.setPythonTag('zone', base.player.graveyard)
            c.reparentTo(self.playerGraveyard)
            c.setPosHpr(0, 0, 0, 0, 0, 0)

            for c1 in base.player.graveyard[:-1]:
                if c1.pandaNode is not None:
                    c1.pandaNode.removeNode()
                c1.pandaNode = None

    def makeEnemyGraveyard(self):
        if len(base.enemy.graveyard) > 0:
            cleanup(self.enemyGraveyard)
            c = self.loadCard(base.enemy.graveyard[-1])
            showCard(c)
            c.setPythonTag('zone', base.enemy.graveyard)
            c.reparentTo(self.enemyGraveyard)
            c.setPosHpr(0, 0, 0, 0, 0, 0)

            for c1 in base.enemy.graveyard[:-1]:
                if c1.pandaNode is not None:
                    c1.pandaNode.removeNode()
                c1.pandaNode = None

    def focusCard(self, card):
        """
        Draws a big version of the card so the player can read the text
        easily.
        """
        # If the node path is pointing to the right card, don't rebuild
        if (card != self.focusedCard and
                card.getPythonTag('_zone') is not
                self.focusedCard.getTag('_zone')):
            self.focusedCard.unstash()
            if len(self.focusedCard.children) > 0:
                self.focusedCard.children[0].removeNode()

            oldCard = self.focusedCard.getPythonTag('oldCard')
            if oldCard:
                oldCard.show()
            # Make a duplicate of the node. Actually a different node path
            # pointing to the same node
            copy = card.copyTo(card.getParent())
            if card.getPythonTag('zone') is base.player.hand:
                copy.setPos(card, 0, -0.2, 1)
                copy.setHpr(0, 0, 0)
                copy.setScale(2.5)
                copy.wrtReparentTo(self.focusedCard)
                self.focusedCard.setPythonTag('oldCard', card)
                card.hide()
            elif card.getPythonTag('zone') is base.enemy.hand:
                copy.setPos(card, 0, -0.2, 0)
                copy.setHpr(0, 0, 0)
                copy.setScale(2.5)
                copy.wrtReparentTo(self.focusedCard)
                self.focusedCard.setPythonTag('oldCard', card)
                card.hide()
            elif card.getPythonTag('zone') is base.enemy.graveyard:
                # Don't get cut off by top of screen
                copy.wrtReparentTo(self.focusedCard)
                copy.setPos(copy, 1.5, -1, -2)
                copy.setHpr(0, 0, 0)
                copy.setScale(2.5)
            else:
                copy.wrtReparentTo(self.focusedCard)
                copy.setPos(copy, 1.5, -1, 1)
                copy.setHpr(0, 0, 0)
                copy.setScale(2.5)
            # Don't try to play this
            self.focusedCard.setCollideMask(BitMask32(0x0))
            # Keep track of the zone to know if it's changed
            # _zone rather than zone so MouseHandler will grab the card under it
            self.focusedCard.setPythonTag('_zone', card.getPythonTag('zone'))

    def unfocusCard(self):
        # Stash the enlarged card image so it won't collide or be visible.
        # This is different from using hide() because it also prevents
        # collision.
        self.focusedCard.stash()
        c = self.focusedCard.getPythonTag('oldCard')
        if c:
            c.show()

    def loadCard(self, card):
        if card.pandaNode is not None:
            showCard(card.pandaNode)
            cardBuilder.updateCard(card)
            return card.pandaNode

        return cardBuilder.buildCard(card, self.scene)

    def loadEnemyBlank(self, card):
        return cardBuilder.buildBlankCard(card, self.scene)

    def makePlayerFace(self):
        cm = CardMaker("face")
        cardModel = self.playerFace.attachNewNode(cm.generate())
        path = base.playerIconPath + "/" + base.playerCardBack
        tex = loader.loadTexture(path)
        cardModel.setTexture(tex)
        self.playerFace.setPythonTag('zone', base.player.face)
        cardModel.setPos(-0.5, 0, -0.5)
        base.playerFaceNode = cardModel
        base.playerFaceNode.setCollideMask(cardBuilder.cardCollisionMask)

    def makeEnemyFace(self):
        cm = CardMaker("face")
        cardModel = self.enemyFace.attachNewNode(cm.generate())
        path = base.enemyIconPath + "/" + base.enemyCardBack
        tex = loader.loadTexture(path)
        cardModel.setTexture(tex)
        self.enemyFace.setPythonTag('zone', base.enemy.face)
        cardModel.setPos(-0.5, 0, -0.5)
        base.enemyFaceNode = cardModel
        # Want it to be possible to click on enemy face
        base.enemyFaceNode.setCollideMask(cardBuilder.cardCollisionMask)

    def redrawAll(self):
        if self.player.hasMulliganed:
            self.makePlayerHand()
        else:
            self.makeMulliganHand()
        self.makeBoard()
        self.makeEnemyHand()
        self.makeEnemyBoard()
        self.makePlayerGraveyard()
        self.makeEnemyGraveyard()

        for n in self.orphan.children:
            n.removeNode()

    def unmake(self):
        self.playerHand.removeNode()  # In case it's parented to the camera
        self.mulliganHand.removeNode()
        base.taskMgr.remove('ResizeMulliganHand')

    def animateDie(self, card):
        if card.pandaNode is None:
            cardBuilder.buildCard(card, self.scene)

        gy = self.playerGraveyard if card.owner is self.player else self.enemyGraveyard

        return animations.animateMove(card.pandaNode, gy, 0.3)

    def animateRevealFacedown(self, card):
        if card.pandaNode is None:
            cardBuilder.buildCard(card, self.scene)

        self.makeBoard()
        self.makeEnemyBoard()

        return animations.animateRevealFacedown(card.pandaNode, 0.3)

    def animatePlayFaceup(self, card):
        if card.pandaNode is None:
            cardBuilder.buildCard(card, base.zoneMaker.scene)

        self.makePlayerHand()
        self.makeBoard()
        self.makeEnemyBoard()

        return animations.animatePlayFaceup(card.pandaNode, 0.3)
