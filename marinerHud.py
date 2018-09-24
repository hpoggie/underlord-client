from ul_core.core.game import Phase
from hud import GameHud


class MarinerHud(GameHud):
    def onFishButton(self):
        base.endPhase(fish=True)

    def redraw(self):
        super().redraw()

        if not hasattr(self, 'fishButton'):
            self.fishButton = self.button(
                text="End and Fish",
                scale=1,
                pos=(0, 0, -1),
                parent=self.endPhaseButton,
                command=self.onFishButton)

        if (base.phase == Phase.reveal and
                base.active and
                base.bothPlayersMulliganed and
                not base.hasFirstPlayerPenalty):
            self.fishButton.show()
        else:
            self.fishButton.hide()
