import ul_core.factions
from ul_core.core.card import Card


class RpcReceiver:
    """
    Translates server messages into game state changes
    """
    def __init__(self, state):
        self.state = state
        self.listeners = []

    def idsToCards(self, cardIds):
        idAndEnemy = zip(cardIds[::2], cardIds[1::2])
        cards = []
        for cardId, ownedByEnemy in idAndEnemy:
            if cardId == -1:
                cards.append(
                    Card(
                        name="mysterious card",
                        owner=self.state.enemy,
                        game=self.state.game,
                        cardId=-1))
            else:
                c = (self.state.enemy.referenceDeck[cardId] if ownedByEnemy
                     else self.state.player.referenceDeck[cardId])
                c.visible = True
                cards.append(c)

        return cards

    def moveCard(self, c, zone):
        # fake moveToZone
        if c._zone is not None and c in c._zone:
            c.prevZone = c._zone
            c._zone.remove(c)
        c._zone = zone
        zone.append(c)

        return c

    def updateZone(self, zone, cardIds):
        zone[:] = []
        for x in self.idsToCards(cardIds):
            self.moveCard(x, zone)

    def onGameEnded(self):
        self.state.ready = False

    # Events
    # Call the callbacks

    def onEnteredGame(self):
        for listener in self.listeners:
            listener.onEnteredGame()

    def updateNumPlayers(self, n):
        for listener in self.listeners:
            listener.updateNumPlayers(n)

    def requestGoingFirstDecision(self):
        for listener in self.listeners:
            listener.requestGoingFirstDecision()

    def enemyGoingFirst(self):
        self.state.onGameStarted(goingFirst=False)
        for listener in self.listeners:
            listener.enemyGoingFirst()

    def enemyGoingSecond(self):
        self.state.onGameStarted(goingFirst=True)
        for listener in self.listeners:
            listener.enemyGoingSecond()

    def requestTarget(self):
        pass

    def requestReplace(self, nArgs):
        for listener in self.listeners:
            listener.requestReplace(nArgs)

    def winGame(self):
        self.onGameEnded()
        for listener in self.listeners:
            listener.winGame()

    def loseGame(self):
        self.onGameEnded()
        for listener in self.listeners:
            listener.loseGame()

    def kick(self):
        self.onGameEnded()
        for listener in self.listeners:
            listener.kick()

    def endRedraw(self):
        for listener in self.listeners:
            listener.endRedraw()
        for c in self.state.player.referenceDeck:
            if c.prevZone is not None:
                for listener in self.listeners:
                    listener.onCardMoved(c, c.prevZone)
                c.prevZone = None

    # Updates
    # Don't call the callbacks, just modify state
    # We redraw things all at once in endRedraw
    def updateEnemyFaction(self, index):
        self.state.enemyFaction = ul_core.factions.availableFactions[index]

    def updateBothPlayersMulliganed(self):
        for pl in self.state.game.players:
            pl.hasMulliganed = True

    def updatePlayerHand(self, *cardIds):
        self.updateZone(self.state.player.hand, cardIds)

    def updateEnemyHand(self, *cardIds):
        self.updateZone(self.state.enemy.hand, cardIds)

    def updatePlayerFacedowns(self, *cardIds):
        self.updateZone(self.state.player.facedowns, cardIds)

    def updateEnemyFacedowns(self, *cardIds):
        self.updateZone(self.state.enemy.facedowns, cardIds)

    def updatePlayerFaceups(self, *cardIds):
        self.updateZone(self.state.player.faceups, cardIds)

    def updateHasAttacked(self, *values):
        for i, c in enumerate(self.state.player.faceups):
            c.hasAttacked = values[i]

    def updateEnemyFaceups(self, *cardIds):
        self.updateZone(self.state.enemy.faceups, cardIds)

    def updatePlayerGraveyard(self, *cardIds):
        self.updateZone(self.state.player.graveyard, cardIds)

    def updateEnemyGraveyard(self, *cardIds):
        self.updateZone(self.state.enemy.graveyard, cardIds)

    def updatePlayerManaCap(self, manaCap):
        self.state.player.manaCap = manaCap

    def updatePlayerMana(self, mana):
        self.state.player.mana = mana

    def updateEnemyManaCap(self, manaCap):
        self.state.enemy.manaCap = manaCap

    def updatePhase(self, phase):
        self.state.phase = phase

    def updatePlayerCounter(self, index, value):
        self.state.player.faceups[index].counter = value

    def updateEnemyCounter(self, index, value):
        self.state.enemy.faceups[index].counter = value

    def setActive(self, value):
        self.state.active = value
