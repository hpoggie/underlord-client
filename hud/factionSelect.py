from . import hud


class FactionSelect(hud.Scene):
    def __init__(self):
        super().__init__()

        self.label(
            text="faction select",
            pos=(0, -0.7, 0),
            mayChange=True)

        icons = self.root.attachNewNode('icons')
        icons.setPos(-0.15 * len(base.availableFactions) / 2, 0, 0)

        for i, faction in enumerate(base.availableFactions):
            self.button(
                image=faction.iconPath + '/' + faction.cardBack,
                parent=icons,
                pos=(i * 0.2, 0, 0),
                relief=None,
                command=base.pickFaction,
                extraArgs=[i])

    def showWaitMessage(self):
        self.label(
            text="Waiting for opponent.",
            pos=(0, -0.5, 0))
