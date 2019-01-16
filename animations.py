from direct.interval.IntervalGlobal import Sequence, Func


def enableFocus(cardNode):
    cardNode.setPythonTag('disableFocus', False)

def animateMove(card, zone, duration):
    card.wrtReparentTo(zone)
    card.setHpr(0, 0, 0)
    Sequence(card.posInterval(duration / 2, (0, 0, 0))).start()

def animateRevealFacedown(card, duration):
    card.setPythonTag('disableFocus', True)
    card.setHpr(180, 0, 0)
    Sequence(card.hprInterval(duration / 2, (0, 0, 0)), Func(enableFocus, card)).start()
