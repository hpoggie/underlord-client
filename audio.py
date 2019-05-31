from direct.showbase.DirectObject import DirectObject

from ul_core.factions.mariners import Mariner


class AudioMaster(DirectObject):
    def __init__(self):
        self.illegalMoveSound = loader.loadSfx('sounds/nope_bad.wav')
        self.clickSound = loader.loadSfx(
            'sounds/108317__robinhood76__02030-swooshing-punch.wav')
        self.startFishSound = loader.loadSfx('assets/sounds/factionAbility_mariner01.wav')
        self.endFishSound = loader.loadSfx('assets/sounds/factionAbility_mariner02.wav')

    def playIllegalMove(self):
        self.illegalMoveSound.play()

    def playDecision(self):
        if isinstance(base.player, Mariner):
            self.endFishSound.play()
