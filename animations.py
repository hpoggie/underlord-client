from direct.interval.IntervalGlobal import Sequence, Parallel, Func
from direct.showbase.DirectObject import DirectObject
from panda3d.core import LVecBase3f

from ul_core.core.card import Card
from scenes.fanHand import fanHand


def animation(func):
    def new_func(*args, **kwargs):
        newArgs = []

        cards = args
        for card in cards:
            if isinstance(card, Card):
                if card.cardId < 0:
                    base.zoneMaker.loadEnemyBlank(card)
                else:
                    base.zoneMaker.loadCard(card)

                newArgs.append(card.pandaNode)
            elif card == base.player.face:
                newArgs.append(base.zoneMaker.playerFace)
            elif card == base.player.opponent.face:
                newArgs.append(base.zoneMaker.enemyFace)
            else:
                newArgs.append(card)

        return func(*newArgs, **kwargs)

    return new_func


def enableFocus(cardNode):
    cardNode.setPythonTag('disableFocus', False)


@animation
def animateFight(attacker, target, duration=0.3):
    oldPos = attacker.getPos()
    return Sequence(attacker.posInterval(duration / 2, target.getPos(attacker.parent)),
                    attacker.posInterval(duration / 2, oldPos))


@animation
def animateMove(card, zone, duration=0.3):
    card.wrtReparentTo(zone)
    card.setHpr(0, 0, 0)
    return Sequence(card.posInterval(duration / 2, (0, 0, 0)))


def animateDie(card, duration=0.3):
    gy = (base.zoneMaker.playerGraveyard
        if card.owner is base.zoneMaker.player else base.zoneMaker.enemyGraveyard)

    return animateMove(card, gy, duration=duration)


def animateFizzle(card, duration=0.3):
    return animateDie(card, duration=duration)


def animateChangeController(card, duration=0.3):
    if card.controller is base.player:
        zone = base.zoneMaker.enemyBoard
    else:
        zone = base.zoneMaker.playerBoard

    return animateMove(card, zone, duration=duration)


@animation
def animateRevealFacedown(card, duration=0.3):
    card.setPythonTag('disableFocus', True)
    card.setHpr(180, 0, 0)
    return Sequence(
        card.posInterval(duration / 3,
                        (card.getX(), card.getY() - 1, card.getZ())),
        card.hprInterval(duration / 3, (0, 0, 0)),
        card.posInterval(duration / 3, card.getPos()),
        Func(enableFocus, card))


@animation
def animatePlayFaceup(card, duration=0.3):
    card.setHpr(0, 0, 0)
    oldPos = card.getPos()
    card.setPos(card, 0, -1, 0)
    return Sequence(card.posInterval(duration / 2, oldPos))


@animation
def animateDraw(card, duration=0.3):
    hand = base.zoneMaker.playerHand\
        if base.bothPlayersMulliganed else base.zoneMaker.mulliganHand
    card.setPos(base.zoneMaker.playerFace, 0, 0, 0)
    card.wrtReparentTo(hand)

    if base.bothPlayersMulliganed:
        fan = fanHand(len(base.player.hand) + 1)[-1]
    else:
        fan = (len(base.player.hand) * 1.1, 0, 0, 0, 0, 0)

    pos, hpr = fan[:3], fan[3:]
    newPos = LVecBase3f(*pos)
    newHpr = LVecBase3f(*hpr)
    return Sequence(Parallel(card.posInterval(duration / 2, newPos),
                            card.hprInterval(duration / 2, newHpr)))


@animation
def animateEnemyDraw(card, duration=0.3):
    hand = base.zoneMaker.enemyHand
    card.setPos(base.zoneMaker.enemyFace, 0, 0, 0)
    card.wrtReparentTo(hand)

    if base.bothPlayersMulliganed:
        fan = fanHand(len(base.enemy.hand) + 1)[-1]
    else:
        fan = (len(base.enemy.hand) * 1.1 / 2, 0, 0, 0, 0, 0)

    pos, hpr = fan[:3], fan[3:]
    newPos = LVecBase3f(*pos)
    newHpr = LVecBase3f(*hpr)
    return Sequence(Parallel(card.posInterval(duration / 2, newPos),
                            card.hprInterval(duration / 2, newHpr)))
