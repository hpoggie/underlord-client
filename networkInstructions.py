import copy


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

    def updateEnemyFaction(self, faction):
        self.base.enemyFaction = faction

    def enemyGoingFirst(self):
        self.base.onGameStarted(goingFirst=False)

    def enemyGoingSecond(self):
        self.base.onGameStarted(goingFirst=True)

    def updateBothPlayersMulliganed(self):
        self.base.bothPlayersMulliganed = True

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

    def endRedraw(self):
        self.base.redraw()
