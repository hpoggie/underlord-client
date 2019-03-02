from panda3d.core import TextNode

from ul_core.core.game import Phase
from ul_core.core.exceptions import IllegalMoveError

from scenes.zoneMaker import hideCard, showCard
from . import hud


class GameHud(hud.Scene):
    def __init__(self, clientState):
        super().__init__()
        self.clientState = clientState

        self.turnLabel = self.label(
            text="",
            pos=(0, -0.8, 0),
            mayChange=True)

        self.playerManaCapLabel = self.label(
            text=str(base.player.manaCap),
            pos=(-0.7, -0.7, 0),
            mayChange=True)
        self.enemyManaCapLabel = self.label(
            text=str(base.enemy.manaCap),
            pos=(-0.5, 0.8),
            mayChange=True)
        self.cardNameLabel = self.label(
            text="",
            pos=(-0.7, -0.6, 0),
            scale=0.07,
            mayChange=True)
        self.tooltipLabel = self.label(
            text="",
            pos=(0, -0.85, 0),
            scale=0.05,
            wordwrap=15,
            mayChange=True)
        self.cardStatsLabel = self.label(
            text="",
            pos=(-0.7, -0.7, 0),
            scale=0.07,
            mayChange=True)
        self.endPhaseLabel = self.label(
            text="",
            pos=(0.7, -0.7, 0),
            mayChange=True)
        self.endPhaseButton = self.button(
            text="End Phase",
            pos=(0.7, 0, -0.85),
            command=self.onEndPhaseButton)
        self.mulliganButton = self.button(
            text="Mulligan",
            pos=(0.7, 0, -0.85),
            command=self.onMulliganButton)

        self.redraw()

    def onMulliganButton(self):
        base.mulligan()

    def onEndPhaseButton(self):
        try:
            base.endPhase()
        except IllegalMoveError as e:
            print(e)

    def hideBigMessage(self):
        base.zoneMaker.playerHand.show()  # hidden by showBigMessage
        if hasattr(self, 'winLabel') and self.winLabel is not None:
            self.winLabel.detachNode()

    def showTargeting(self):
        if not hasattr(self, 'targetingLabel'):
            self.targetingLabel = self.label(
                pos=(0, 0, 0),
                mayChange=True)
            self.targetingGradient = self.image(
                image="gradient.png",
                pos=(0, -0.7, 0),
                scale=(10, 1, 3))
        else:
            self.targetingLabel.show()
            self.targetingGradient.show()

        self.targetingLabel.setText(base.targetDesc.split('\n')[0])

    def hideTargeting(self):
        self.targetingLabel.hide()
        self.targetingGradient.hide()

    def redrawTooltips(self):
        if not base.gameState.hasMulliganed:
            self.tooltipLabel.setText("Replace cards you don't want in your opening hand")
        elif self.clientState.active:
            if base.phase == Phase.startOfTurn:
                text = "Use your faction ability or proceed to your reveal phase"
            elif base.phase == Phase.reveal:
                text = "Reveal face-down cards or play fast cards"
            else:
                text = "Play face-down cards and attack with units"

            self.tooltipLabel.setText(text)
        else:
            self.tooltipLabel.setText("")

    def redraw(self):
        if base.gameState.hasMulliganed:
            self.mulliganButton.detachNode()
            self.endPhaseLabel.setText(str(Phase.keys[base.phase]))
        else:
            self.endPhaseLabel.setText("Mulligan")

        self.redrawTooltips()

        # Hide everything if we haven't mulliganed yet
        if not base.bothPlayersMulliganed:
            self.endPhaseButton.hide()
            self.playerManaCapLabel.setText("")
            self.enemyManaCapLabel.setText("")
            return

        if self.clientState.active:
            self.endPhaseButton.show()
        else:
            self.endPhaseButton.hide()

        if base.phase == Phase.reveal and self.clientState.active:
            self.playerManaCapLabel.setText(
                str(base.player.mana) + " / " + str(base.player.manaCap))
        else:
            self.playerManaCapLabel.setText(str(base.player.manaCap))

        self.enemyManaCapLabel.setText(str(base.enemy.manaCap))
        self.turnLabel.setText("Your Turn" if self.clientState.active else "Enemy Turn")

    def startTargeting(self, nTargets):
        targets = []

        def callback(target):
            if target in targets:
                targets.remove(target)
                if target is not None:
                    showCard(target)
            else:
                targets.append(target)
                if target is not None:
                    hideCard(target)

            if len(targets) == nTargets:
                base.makeDecision(targets)
                base.finishTargeting()

        # TODO: base on desc for effect
        base.mouseHandler.startTargeting("Select targets", callback)
