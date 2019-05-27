import animations


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

    def onCardMoved(self, card, prevZone):
        if card.faceup and (prevZone == card.controller.facedowns
                            or prevZone == card.controller.opponent.facedowns):
            animations.animateRevealFacedown(card.pandaNode, 0.3)
        elif card.faceup:
            animations.animatePlayFaceup(card.pandaNode, 0.3)

    def playAnimation(self, *args):
        class Animations:
            def on_spawn(card):
                self.onCardMoved(card, card.zone)

            def on_fight(attacker, target):
                pass

            def on_die(card):
                pass

            def on_change_controller(card):
                pass

            def on_reveal_facedown(card, target=None):
                pass

            def on_play_faceup(card, target=None):
                pass

            def on_play_facedown(card):
                pass

            def on_draw(card):
                pass

            def on_end_turn():
                pass

        getattr(Animations, args[0])(*args[1:])
