from direct.interval.IntervalGlobal import Sequence, Func


def animateMove(card, zone, duration):
    card.wrtReparentTo(zone)
    card.setHpr(0, 0, 0)
    Sequence(card.posInterval(duration / 2, (0, 0, 0))).start()

def animateRevealFacedown(card, duration):
    card.setHpr(180, 0, 0)
    Sequence(card.hprInterval(duration / 2, (0, 0, 0))).start()
