import ul_core.factions
from . import update_queue
from ul_core.core.card import Card


def setup_card_args(args):
    # Give all the mysterious cards pandaNodes so other stuff doesn't complain
    for arg in args:
        if isinstance(arg, Card) and not hasattr(arg, 'pandaNode'):
            arg.pandaNode = None


def queued_update(func):
    def do_update(self, *args, **kwargs):
        setup_card_args(args)
        update_queue.do_later(lambda: func(self, *args, **kwargs))

    return do_update


class RpcReceiver:
    """
    Translates server messages into game state changes
    """
    def __init__(self, state):
        self.state = state
        self.listeners = []

    def moveCard(self, c, zone):
        if c is None:
            return c

        # fake moveToZone
        if c._zone is not None and c in c._zone:
            c._zone.remove(c)
        c._zone = zone
        zone.append(c)

        return c

    def updateZone(self, zone, cards):
        zone[:] = []
        for x in cards:
            self.moveCard(x, zone)

    def onGameEnded(self):
        self.state.ready = False

    # Events
    # Call the callbacks

    def onEnteredGame(self):
        for listener in self.listeners:
            listener.onEnteredGame()

    def updateNumPlayers(self, n):
        for listener in self.listeners:
            listener.updateNumPlayers(n)

    def requestGoingFirstDecision(self):
        for listener in self.listeners:
            listener.requestGoingFirstDecision()

    def enemyGoingFirst(self):
        self.state.onGameStarted(goingFirst=False)
        for listener in self.listeners:
            listener.enemyGoingFirst()

    def enemyGoingSecond(self):
        self.state.onGameStarted(goingFirst=True)
        for listener in self.listeners:
            listener.enemyGoingSecond()

    def requestTarget(self):
        pass

    def requestDecision(self, nArgs):
        for listener in self.listeners:
            update_queue.do_later(lambda: listener.requestDecision(nArgs))

        # We get this after endRedraw, so we need to start the update queue again
        # since all the animations have already finished
        update_queue.start()

    def winGame(self):
        self.onGameEnded()
        for listener in self.listeners:
            listener.winGame()

    def loseGame(self):
        self.onGameEnded()
        for listener in self.listeners:
            listener.loseGame()

    def kick(self):
        self.onGameEnded()
        for listener in self.listeners:
            listener.kick()

    def endRedraw(self):
        def after_updates_finished():
            self.state.player.fishing = False
            for listener in self.listeners:
                listener.endRedraw()

        update_queue.do_later(after_updates_finished)

        update_queue.start()

    def playAnimation(self, *args):
        class AnimCallback:
            def on_spawn():
                pass

            def on_fight():
                pass

            def on_die():
                return self.moveCard(args[1], args[1].owner.graveyard)

            def on_fizzle():
                return self.moveCard(args[1], args[1].owner.graveyard),

            def on_change_controller():
                # TODO: do this in a cleaner way
                # This works because anything after (on_spawn, on_die, etc.) will set the zone
                return self.moveCard(
                    args[1],
                    args[1].controller.opponent.faceups)

            def on_reveal_facedown():
                return self.moveCard(args[1], args[1].controller.faceups)

            def on_play_faceup():
                return self.moveCard(args[1], args[1].controller.faceups)

            def on_play_facedown():
                return self.moveCard(args[1], args[1].controller.facedowns)

            def on_draw():
                return self.moveCard(args[1], args[1].controller.hand)

            def on_end_turn():
                pass

        update_queue.do_later(getattr(AnimCallback, args[0]))

        setup_card_args(args)
        for listener in self.listeners:
            update_queue.do_later(lambda: listener.playAnimation(*args))

    def illegalMove(self):
        for listener in self.listeners:
            listener.illegalMove()

    # Updates
    # Don't call the callbacks, just modify state
    # We redraw things all at once in endRedraw
    def updateEnemyFaction(self, index):
        self.state.enemyFaction = ul_core.factions.availableFactions[index]

    def updateBothPlayersMulliganed(self):
        for pl in self.state.game.players:
            pl.hasMulliganed = True

    @queued_update
    def updatePlayerHand(self, *cards):
        self.updateZone(self.state.player.hand, cards)

    @queued_update
    def updateEnemyHand(self, *cards):
        self.updateZone(self.state.enemy.hand, cards)

    @queued_update
    def updatePlayerFacedowns(self, *cards):
        self.updateZone(self.state.player.facedowns, cards)

    @queued_update
    def updateEnemyFacedowns(self, *cards):
        self.updateZone(self.state.enemy.facedowns, cards)

    @queued_update
    def updatePlayerFaceups(self, *cards):
        self.updateZone(self.state.player.faceups, cards)

    @queued_update
    def updateHasAttacked(self, *values):
        for i, c in enumerate(self.state.player.faceups):
            c.hasAttacked = values[i]

    @queued_update
    def updateEnemyFaceups(self, *cards):
        self.updateZone(self.state.enemy.faceups, cards)

    @queued_update
    def updatePlayerGraveyard(self, *cards):
        self.updateZone(self.state.player.graveyard, cards)

    @queued_update
    def updateEnemyGraveyard(self, *cards):
        self.updateZone(self.state.enemy.graveyard, cards)

    @queued_update
    def updatePlayerManaCap(self, manaCap):
        self.state.player.manaCap = manaCap

    @queued_update
    def updatePlayerMana(self, mana):
        self.state.player.mana = mana

    @queued_update
    def updateEnemyManaCap(self, manaCap):
        self.state.enemy.manaCap = manaCap

    @queued_update
    def updatePlayerCounter(self, index, value):
        self.state.player.faceups[index].counter = value

    @queued_update
    def updateEnemyCounter(self, index, value):
        self.state.enemy.faceups[index].counter = value

    @queued_update
    def updatePlayerFacedownStaleness(self, *values):
        for i, c in enumerate(self.state.player.facedowns):
            c.stale = values[i]

    @queued_update
    def updateEnemyFacedownStaleness(self, *values):
        for i, c in enumerate(self.state.enemy.facedowns):
            c.stale = values[i]

    @queued_update
    def setActive(self, value):
        self.state.active = value
