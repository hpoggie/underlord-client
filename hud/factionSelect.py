from . import hud


class FactionSelect(hud.Scene):
    def __init__(self, availableFactions):
        super().__init__()

        self.label(
            text="faction select",
            pos=(0, -0.7, 0),
            mayChange=True)

        icons = self.root.attachNewNode('icons')
        icons.setPos(-0.155 * len(availableFactions) / 2 + 0.005, 0, 0)

        for i, faction in enumerate(availableFactions):
            self.button(
                image=faction.iconPath + '/' + faction.cardBack,
                parent=icons,
                pos=(i * 0.21, 0, 0),
                relief=None,
                command=base.pickFaction,
                extraArgs=[i],
                clickSound=faction.selectSound)

    def showWaitMessage(self):
        self.label(
            text="Waiting for opponent.",
            pos=(0, -0.5, 0))

    def onKicked(self):
        self.showBigMessage("Kicked")
