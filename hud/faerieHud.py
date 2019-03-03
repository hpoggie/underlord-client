import hud.game


class FaerieHud(hud.game.GameHud):
    def onEndTurnButton(self):
        def callback(card):
            base.endTurn(card)
            base.finishTargeting()

        if len(base.player.facedowns) == 0:
            super().onEndTurnButton()
        elif len(base.player.facedowns) == 1:
            base.clientActions.endTurn([base.player.facedowns[0]])
        else:
            base.mouseHandler.startTargeting("Choose card to keep", callback)
