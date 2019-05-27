import queue
import ul_core.factions


def queued_update(func):
    def do_update(self, *args, **kwargs):
        self.update_queue.put(lambda: func(self, *args, **kwargs))

    return do_update


class RpcReceiver:
    """
    Translates server messages into game state changes
    """
    def __init__(self, state):
        self.state = state
        self.listeners = []
        self.update_queue = queue.Queue()

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
            listener.requestDecision(nArgs)

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
        while True:
            try:
                self.update_queue.get_nowait()()
            except queue.Empty:
                break

        self.state.player.fishing = False
        for listener in self.listeners:
            listener.endRedraw()

    def playAnimation(self, *args):
        def make_update_func(args):
            def _pr():
                print("playAnimation " + " ".join(str(i) for i in args))
                for listener in self.listeners:
                    listener.playAnimation(*args)

            def set_zone(card, zone):
                card.zone = zone
                _pr()

            return {
                'on_spawn': _pr,
                'on_fight': _pr,  # TODO play the fight animation
                'on_die': lambda: set_zone(args[1], args[1].owner.graveyard),
                # TODO: do this in a cleaner way
                # This works because anything after (on_spawn, on_die, etc.) will set the zone
                'on_change_controller': lambda: set_zone(
                    args[1],
                    args[1].controller.opponent.faceups),
                'on_reveal_facedown': lambda: set_zone(args[1], args[1].controller.faceups),
                'on_play_faceup': lambda: set_zone(args[1], args[1].controller.faceups),
                'on_play_facedown': lambda: set_zone(args[1], args[1].controller.facedowns),
                'on_draw': _pr, # TODO: anim
                'on_end_turn': _pr
            }[args[0]]

        self.update_queue.put(make_update_func(args))

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
