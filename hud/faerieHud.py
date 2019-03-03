import hud.game


class FaerieHud(hud.game.GameHud):
    def onEndTurnButton(self):
        def callback(card):
            base.endTurn(card)
            base.finishTargeting()

        staleFds = [fd for fd in base.player.facedowns if fd.stale]

        if len(staleFds) == 0:
            super().onEndTurnButton()
        elif len(staleFds) == 1:
            base.clientActions.endTurn([staleFds[0]])
        else:
            base.mouseHandler.startTargeting("Choose card to keep", callback)
