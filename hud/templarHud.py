from ul_core.core.game import Phase
from ul_core.core.exceptions import IllegalMoveError
import ul_core.factions.templars
from hud.game import GameHud


class TemplarHud(GameHud):
    def onEndPhaseButton(self):
        try:
            base.endPhase(card=None)
        except IllegalMoveError as e:
            print(e)

    def onTemplarEndPhaseButton(self):
        def callback(target):
            try:
                base.endPhase(card=target)
            except IllegalMoveError as e:
                print(e)
            else:
                base.finishTargeting()

        # TODO: grab desc from faction?
        base.mouseHandler.startTargeting(
            "Choose a card to discard.",
            callback)


    def redraw(self):
        super().redraw()

        if not hasattr(self, 'templarEndPhaseButton'):
            self.templarEndPhaseButton = self.button(
                text="Faction Ability",
                scale=1,
                pos=(0, 0, -1),
                parent=self.endPhaseButton,
                command=self.onTemplarEndPhaseButton)

        # Hide everything if we haven't mulliganed yet
        if not base.bothPlayersMulliganed:
            self.templarEndPhaseButton.hide()
            return

        if base.phase == Phase.play and self.clientState.active:
            self.templarEndPhaseButton.show()
        else:
            self.templarEndPhaseButton.hide()

