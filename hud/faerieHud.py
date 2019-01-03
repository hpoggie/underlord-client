from ul_core.core.game import Phase

import hud.game


class FaerieHud(hud.game.GameHud):
    def onEndPhaseButton(self):
        if self.clientState.game.phase != Phase.reveal:
            base.clientActions.endPhase([])
            return

        def callback(card):
            base.endPhase(card)
            base.finishTargeting()

        if len(base.player.facedowns) == 0:
            super().onEndPhaseButton()
        elif len(base.player.facedowns) == 1:
            base.clientActions.endPhase([base.player.facedowns[0]])
        else:
            base.mouseHandler.startTargeting("Choose card to keep", callback)
