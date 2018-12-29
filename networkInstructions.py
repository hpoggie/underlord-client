import copy

from ul_core.core.card import Card
from ul_core.core.game import EndOfGame
from ul_core.core.zone import Zone


class NetworkInstructions:
    """
    Handles instructions from the server.
    """

    def __init__(self, base):
        self.base = base

    def onEnteredGame(self):
        self.base.onEnteredGame()

    def updateNumPlayers(self, n):
        # numPlayersLabel is set by hud
        if hasattr(self.base, 'numPlayersLabel') and self.base.numPlayersLabel:
            self.base.numPlayersLabel.setText(str(n) + " players in lobby.")

    def requestGoingFirstDecision(self):
        self.base.decideWhetherToGoFirst()

    def updateEnemyFaction(self, index):
        self.base.enemyFaction = self.base.availableFactions[index]

    def enemyGoingFirst(self):
        self.base.onGameStarted(goingFirst=False)

    def enemyGoingSecond(self):
        self.base.onGameStarted(goingFirst=True)

    def updateBothPlayersMulliganed(self):
        self.base.bothPlayersMulliganed = True

    def idsToCards(self, cardIds):
        idAndEnemy = zip(cardIds[::2], cardIds[1::2])
        cards = []
        for cardId, ownedByEnemy in idAndEnemy:
            if cardId == -1:
                cards.append(Card(name="mysterious card",
                             owner=self.base.enemy,
                             game=self.base.game,
                             cardId=-1))
            else:
                c = (self.base.enemy.referenceDeck[cardId] if ownedByEnemy
                     else self.base.player.referenceDeck[cardId])
                c.visible = True
                cards.append(c)

        return cards

    def moveCard(self, c, zone):
        # fake moveToZone
        if c._zone is not None and c in c._zone:
            c._zone.remove(c)
        c._zone = zone
        zone.append(c)

        return c

    def updatePlayerHand(self, *cardIds):
        self.base.player.hand[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.player.hand)

    def updateEnemyHand(self, *cardIds):
        self.base.enemy.hand[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.enemy.hand)

    def updatePlayerFacedowns(self, *cardIds):
        self.base.player.facedowns[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.player.facedowns)

    def updateEnemyFacedowns(self, *cardIds):
        self.base.enemy.facedowns[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.enemy.facedowns)

    def updatePlayerFaceups(self, *cardIds):
        self.base.player.faceups[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.player.faceups)

    def updateHasAttacked(self, *values):
        for i, c in enumerate(self.base.player.faceups):
            c.hasAttacked = values[i]

    def updateEnemyFaceups(self, *cardIds):
        self.base.enemy.faceups[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.enemy.faceups)

    def updatePlayerGraveyard(self, *cardIds):
        self.base.player.graveyard[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.player.graveyard)

    def updateEnemyGraveyard(self, *cardIds):
        self.base.enemy.graveyard[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, self.base.enemy.graveyard)

    def updatePlayerManaCap(self, manaCap):
        self.base.player.manaCap = manaCap

    def updatePlayerMana(self, mana):
        self.base.player.mana = mana

    def updateEnemyManaCap(self, manaCap):
        self.base.enemy.manaCap = manaCap

    def updatePhase(self, phase):
        self.base.phase = phase

    def updatePlayerCounter(self, index, value):
        self.base.player.faceups[index].counter = value

    def updateEnemyCounter(self, index, value):
        self.base.enemy.faceups[index].counter = value

    def requestTarget(self):
        pass

    def requestReplace(self, nArgs):
        self.base.guiScene.startReplacing(nArgs)

    def winGame(self):
        self.base.guiScene.showBigMessage("Victory")
        self.base.quitToMainMenu()

    def loseGame(self):
        self.base.guiScene.showBigMessage("Defeat")
        self.base.quitToMainMenu()

    def kick(self):
        self.base.guiScene.showBigMessage("Kicked")
        self.base.quitToMainMenu()

    def setActive(self, value):
        self.base.active = value

    def endRedraw(self):
        self.base.redraw()
