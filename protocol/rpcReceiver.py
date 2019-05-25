import ul_core.factions


class RpcReceiver:
    """
    Translates server messages into game state changes
    """
    def __init__(self, state):
        self.state = state
        self.listeners = []

    def moveCard(self, c, zone):
        if c is None:
            return c
               
        # fake moveToZone
        if c._zone is not None and c in c._zone:
            c.prevZone = c._zone
            c._zone.remove(c)
        c._zone = zone
        zone.append(c)

        return c

    def updateZone(self, zone, cards):
        zone[:] = []
        for x in cards:
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

    def requestDecision(self, nArgs):
        for listener in self.listeners:
            listener.requestDecision(nArgs)

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
        self.state.player.fishing = False
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

    def updatePlayerHand(self, *cards):
        self.updateZone(self.state.player.hand, cards)

    def updateEnemyHand(self, *cards):
        self.updateZone(self.state.enemy.hand, cards)

    def updatePlayerFacedowns(self, *cards):
        self.updateZone(self.state.player.facedowns, cards)

    def updateEnemyFacedowns(self, *cards):
        self.updateZone(self.state.enemy.facedowns, cards)

    def updatePlayerFaceups(self, *cards):
        self.updateZone(self.state.player.faceups, cards)

    def updateHasAttacked(self, *values):
        for i, c in enumerate(self.state.player.faceups):
            c.hasAttacked = values[i]

    def updateEnemyFaceups(self, *cards):
        self.updateZone(self.state.enemy.faceups, cards)

    def updatePlayerGraveyard(self, *cards):
        self.updateZone(self.state.player.graveyard, cards)

    def updateEnemyGraveyard(self, *cards):
        self.updateZone(self.state.enemy.graveyard, cards)

    def updatePlayerManaCap(self, manaCap):
        self.state.player.manaCap = manaCap

    def updatePlayerMana(self, mana):
        self.state.player.mana = mana

    def updateEnemyManaCap(self, manaCap):
        self.state.enemy.manaCap = manaCap

    def updatePlayerCounter(self, index, value):
        self.state.player.faceups[index].counter = value

    def updateEnemyCounter(self, index, value):
        self.state.enemy.faceups[index].counter = value

    def updatePlayerFacedownStaleness(self, *values):
        for i, c in enumerate(self.state.player.facedowns):
            c.stale = values[i]

    def updateEnemyFacedownStaleness(self, *values):
        for i, c in enumerate(self.state.enemy.facedowns):
            c.stale = values[i]

    def setActive(self, value):
        self.state.active = value
