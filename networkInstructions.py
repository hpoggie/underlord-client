import cardBuilder


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

    def enemyGoingFirst(self):
        self.base.onGameStarted(goingFirst=False)

    def enemyGoingSecond(self):
        self.base.onGameStarted(goingFirst=True)

    def requestDecision(self, nArgs):
        self.base.guiScene.startTargeting(nArgs)

    def winGame(self):
        self.base.guiScene.showBigMessage("Victory")
        self.base.quitToMainMenu()

    def loseGame(self):
        self.base.guiScene.showBigMessage("Defeat")
        self.base.quitToMainMenu()

    def kick(self):
        self.base.scene.onKicked()
        self.base.quitToMainMenu()

    def endRedraw(self):
        self.base.redraw()

    def playAnimation(self, *args):
        class Animations:
            def on_spawn(card):
                pass

            def on_fight(attacker, target):
                pass

            def on_die(card):
                pass

            def on_change_controller(card):
                pass

            def on_reveal_facedown(card, target=None):
                return self.base.zoneMaker.animateRevealFacedown(card)

            def on_play_faceup(card, target=None):
                return self.base.zoneMaker.animatePlayFaceup(card)

            def on_play_facedown(card):
                pass

            def on_draw(card):
                pass

            def on_end_turn():
                pass

        return getattr(Animations, args[0])(*args[1:])
