from . import zie
import ul_core.factions


class ClientActions:
    def __init__(self, state, rpcSender):
        self.state = state
        self.rpcSender = rpcSender

    @property
    def player(self):
        return self.state.player

    # Setup actions
    def requestNumPlayers(self):
        self.rpcSender.requestNumPlayers()

    def readyUp(self):
        self.rpcSender.addPlayer()
        self.state.ready = True

    def pickFaction(self, index):
        self.rpcSender.selectFaction(index)
        self.state.faction = ul_core.factions.availableFactions[index]

    def goFirst(self):
        self.rpcSender.decideWhetherToGoFirst(1)
        self.state.onGameStarted(goingFirst=True)

    def goSecond(self):
        self.rpcSender.decideWhetherToGoFirst(0)
        self.state.onGameStarted(goingFirst=False)

    def mulligan(self, cards):
        indices = [self.state.player.hand.index(c) for c in cards]
        self.rpcSender.mulligan(*indices)
        self.state.hasMulliganed = True

    # Game actions
    # TODO: Most of this is ugly and should be refactored
    def revealFacedown(self, card, target=None):
        index = card.zone.index(card)
        if target is not None:
            self.rpcSender.revealFacedown(
                index, *zie.gameEntityToZie(self.player, target))
        else:
            self.rpcSender.revealFacedown(index)

    def playFacedown(self, card):
        idx = card.zone.index(card)
        self.rpcSender.play(idx)

    def playFaceup(self, card, target=None):
        idx = card.zone.index(card)

        if target:
            self.rpcSender.playFaceup(
                idx, *zie.gameEntityToZie(self.player, target))
        else:
            self.rpcSender.playFaceup(idx)

    def attack(self, attacker, target):
        _, index, _ = zie.gameEntityToZie(self.player, attacker)
        targetZone, targetIndex, _ = zie.gameEntityToZie(self.player, target)
        self.rpcSender.attack(index, targetIndex, targetZone)

    def endPhase(self, args):
        # For each value in args, append it if it's a bool, otherwise
        # assume it's a card and append the indices for it
        args = [
            i for arg in args
            for i in ([arg] if isinstance(arg, bool) else zie.gameEntityToZie(
                self.player, arg))
        ]

        self.rpcSender.endPhase(*args)

    def replace(self, cards):
        args = [
            i for card in cards
            for i in zie.gameEntityToZie(self.player, card)
        ]
        self.rpcSender.replace(*args)
