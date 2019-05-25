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
        self.rpcSender.mulligan(*cards)
        self.state.hasMulliganed = True

    # Game actions
    def revealFacedown(self, card, target=None):
        self.rpcSender.revealFacedown(card, target)

    def playFacedown(self, card):
        self.rpcSender.play(card)

    def playFaceup(self, card, target=None):
        self.rpcSender.playFaceup(card, target)

    def attack(self, attacker, target):
        self.rpcSender.attack(attacker, target)

    def endTurn(self, args):
        self.rpcSender.endTurn(*args)

    def makeDecision(self, cards):
        self.rpcSender.makeDecision(*cards)

    def useTemplarAbility(self, card):
        self.rpcSender.useFactionAbility(card)

    def useThiefAbility(self, toDiscard, toSteal, cardname):
        self.rpcSender.useFactionAbility(toDiscard, toSteal, cardname)

    def useMarinerAbility(self):
        self.rpcSender.useFactionAbility()
