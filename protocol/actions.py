from . import zie


class ClientActions:
    def __init__(self, player, rpcSender):
        self.player = player
        self.rpcSender = rpcSender

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
