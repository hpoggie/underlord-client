from ul_core.core.game import Game


class ClientState:
    """
    Representation of game state on client side
    """

    def __init__(self):
        self.faction = None
        self.enemyFaction = None
        self.hasMulliganed = False
        self.ready = False

    @property
    def active(self):
        return self.player.active if hasattr(self, 'player') else False

    @active.setter
    def active(self, value):
        """
        Update whose turn it is.
        """
        # Ignore setting active before mulligans
        # b/c the opcode is False instead of None
        # TODO: change this
        if self.hasMulliganed:
            # (not value) gives us 0 for player 1 and 1 for player 2
            self.game.turn = not value if (
                self.player == self.game.players[0]) else value

    @property
    def phase(self):
        return self.game.phase

    @phase.setter
    def phase(self, value):
        self.game.phase = value

    def onGameStarted(self, goingFirst):
        if goingFirst:
            self.game = Game(self.faction, self.enemyFaction)
            self.player, self.enemy = self.game.players
        else:
            self.game = Game(self.enemyFaction, self.faction)
            self.enemy, self.player = self.game.players

        self.hasMulliganed = False
