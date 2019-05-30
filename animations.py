from direct.interval.IntervalGlobal import Sequence, Func


def enableFocus(cardNode):
    cardNode.setPythonTag('disableFocus', False)


def animateFight(attacker, target, duration):
    oldPos = attacker.getPos()
    return Sequence(attacker.posInterval(duration / 2, target.getPos(attacker.parent)),
                    attacker.posInterval(duration / 2, oldPos))


def animateMove(card, zone, duration):
    card.wrtReparentTo(zone)
    card.setHpr(0, 0, 0)
    return Sequence(card.posInterval(duration / 2, (0, 0, 0)))


def animateRevealFacedown(card, duration):
    card.setPythonTag('disableFocus', True)
    card.setHpr(180, 0, 0)
    return Sequence(
        card.posInterval(duration / 3,
                         (card.getX(), card.getY() - 1, card.getZ())),
        card.hprInterval(duration / 3, (0, 0, 0)),
        card.posInterval(duration / 3, card.getPos()), Func(enableFocus,
                                                            card))


def animatePlayFaceup(card, duration):
    card.setHpr(0, 0, 0)
    oldPos = card.getPos()
    card.setPos(card, 0, -1, 0)
    return Sequence(card.posInterval(duration / 2, oldPos))
