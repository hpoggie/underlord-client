from hud.game import GameHud


class MarinerHud(GameHud):
    def onFishButton(self):
        base.useMarinerAbility()

    def redraw(self):
        super().redraw()

        if not hasattr(self, 'fishButton'):
            self.fishButton = self.button(
                text="End and Fish",
                scale=1,
                pos=(0, 0, -1),
                parent=self.endTurnButton,
                command=self.onFishButton,
                clickSound=base.audioMaster.startFishSound)

        if (self.clientState.active and
                base.bothPlayersMulliganed):
            self.fishButton.show()
        else:
            self.fishButton.hide()
