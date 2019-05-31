import cardBuilder
from ul_core.core.card import Card


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
        # Give all the mysterious cards pandaNodes so other stuff doesn't complain
        for arg in args:
            if isinstance(arg, Card) and not hasattr(arg, 'pandaNode'):
                arg.pandaNode = None

        class Animations:
            def on_spawn(card):
                pass

            def on_fight(attacker, target):
                return self.base.cardAnimator.animateFight(attacker, target)

            def on_die(card):
                return self.base.cardAnimator.animateDie(card)

            def on_fizzle(card):
                return self.base.cardAnimator.animateFizzle(card)

            def on_change_controller(card):
                return self.base.cardAnimator.animateChangeController(card)

            def on_reveal_facedown(card, target=None):
                return self.base.cardAnimator.animateRevealFacedown(card)

            def on_play_faceup(card, target=None):
                return self.base.cardAnimator.animatePlayFaceup(card)

            def on_play_facedown(card):
                pass

            def on_draw(card):
                if card.controller == self.base.player:
                    return self.base.cardAnimator.animateDraw(card)
                else:
                    return self.base.cardAnimator.animateEnemyDraw(card)

            def on_end_turn():
                pass

        return getattr(Animations, args[0])(*args[1:])

    def illegalMove(self):
        self.base.audioMaster.playIllegalMove()
