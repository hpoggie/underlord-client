from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.DirectObject import DirectObject
from panda3d.core import LVecBase3f

from scenes.fanHand import fanHand


def animation(func):
    def new_func(self, *args, **kwargs):
        base.zoneMaker.redrawAll()

        cards = args
        for card in cards:
            try:
                base.zoneMaker.loadCard(card)
            except Exception:  # TODO: this is needed because mysterious cards don't update properly
                return

        return func(self, *(card.pandaNode for card in cards), **kwargs)

    return new_func


class CardAnimator(DirectObject):
    def enableFocus(self, cardNode):
        cardNode.setPythonTag('disableFocus', False)

    @animation
    def animateFight(self, attacker, target, duration=0.3):
        oldPos = attacker.getPos()
        return Sequence(attacker.posInterval(duration / 2, target.getPos(attacker.parent)),
                        attacker.posInterval(duration / 2, oldPos))

    @animation
    def animateMove(self, card, zone, duration=0.3):
        card.wrtReparentTo(zone)
        card.setHpr(0, 0, 0)
        return Sequence(card.posInterval(duration / 2, (0, 0, 0)))

    def animateDie(self, card, duration=0.3):
        gy = (base.zoneMaker.playerGraveyard
              if card.owner is base.zoneMaker.player else base.zoneMaker.enemyGraveyard)

        self.animateMove(card, gy, duration=duration)

    @animation
    def animateRevealFacedown(self, card, duration=0.3):
        card.setPythonTag('disableFocus', True)
        card.setHpr(180, 0, 0)
        return Sequence(
            card.posInterval(duration / 3,
                            (card.getX(), card.getY() - 1, card.getZ())),
            card.hprInterval(duration / 3, (0, 0, 0)),
            card.posInterval(duration / 3, card.getPos()),
            Func(self.enableFocus, card))

    @animation
    def animatePlayFaceup(self, card, duration=0.3):
        card.setHpr(0, 0, 0)
        oldPos = card.getPos()
        card.setPos(card, 0, -1, 0)
        return Sequence(card.posInterval(duration / 2, oldPos))

    @animation
    def animateDraw(self, card, duration=0.3):
        card.setPos(base.zoneMaker.playerFace, 0, 0, 0)
        fan = fanHand(len(base.player.hand) + 1)
        newPos = LVecBase3f(*fan[-1][:3]) + base.zoneMaker.playerHand.getPos()
        return Sequence(card.posInterval(duration / 2, newPos))
