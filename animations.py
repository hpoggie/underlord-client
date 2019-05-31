from direct.interval.IntervalGlobal import Sequence, Parallel, Func
from direct.showbase.DirectObject import DirectObject
from panda3d.core import LVecBase3f

from ul_core.core.card import Card
from scenes.fanHand import fanHand


def animation(func):
    def new_func(self, *args, **kwargs):
        base.zoneMaker.redrawAll()

        cards = args
        for card in cards:
            if isinstance(card, Card) and card.cardId < 0:
                base.zoneMaker.loadEnemyBlank(card)
            elif isinstance(card, Card) and card.cardId >= 0:
                base.zoneMaker.loadCard(card)

        return func(self, *(card.pandaNode if isinstance(card, Card) else card for card in cards), **kwargs)

    return new_func


class CardAnimator(DirectObject):
    def __init__(self):
        self.nHandCards = 0
        self.nEnemyHandCards = 0

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

        return self.animateMove(card, gy, duration=duration)

    def animateFizzle(self, card, duration=0.3):
        return self.animateDie(card, duration=duration)

    def animateChangeController(self, card, duration=0.3):
        if card.controller is base.player:
            zone = base.zoneMaker.enemyBoard
        else:
            zone = base.zoneMaker.playerBoard

        return self.animateMove(card, zone, duration=duration)

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
        hand = base.zoneMaker.playerHand\
            if base.bothPlayersMulliganed else base.zoneMaker.mulliganHand
        card.setPos(base.zoneMaker.playerFace, 0, 0, 0)

        if base.bothPlayersMulliganed:
            fan = fanHand(len(base.player.hand) + 1)[-1]
        else:
            fan = (self.nHandCards * 1.1 / 2, 0, 0, 0, 0, 0)
            self.nHandCards += 1

        pos, hpr = fan[:3], fan[3:]
        newPos = LVecBase3f(*pos) + hand.getPos(base.render)
        newHpr = LVecBase3f(*hpr) + hand.getHpr(base.render)
        return Sequence(Parallel(card.posInterval(duration / 2, newPos),
                                 card.hprInterval(duration / 2, newHpr)))

    @animation
    def animateEnemyDraw(self, card, duration=0.3):
        hand = base.zoneMaker.enemyHand
        card.setPos(base.zoneMaker.enemyFace, 0, 0, 0)

        if base.bothPlayersMulliganed:
            fan = fanHand(len(base.enemy.hand) + 1)[-1]
        else:
            fan = (self.nEnemyHandCards * 1.1 / 2, 0, 0, 0, 0, 0)
            self.nHandCards += 1

        pos, hpr = fan[:3], fan[3:]
        newPos = LVecBase3f(*pos) + hand.getPos(base.render)
        newHpr = LVecBase3f(*hpr) + hand.getHpr(base.render)
        return Sequence(Parallel(card.posInterval(duration / 2, newPos),
                                 card.hprInterval(duration / 2, newHpr)))
