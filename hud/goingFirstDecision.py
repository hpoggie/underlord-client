from . import hud


class GoingFirstDecision(hud.Scene):
    def __init__(self):
        super().__init__()

        self.button(
            text="Go first",
            pos=(0, 0, 0.1),
            command=base.goFirst)
        self.button(
            text="Go second",
            pos=(0, 0, -0.1),
            command=base.goSecond)
