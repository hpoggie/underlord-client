from . import zie


class ClientActions:
    def __init__(self, player, rpcSender):
        self.player = player
        self.rpcSender = rpcSender

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
