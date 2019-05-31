from direct.showbase.DirectObject import DirectObject

from ul_core.factions.templars import Templar
from ul_core.factions.thieves import Thief
from ul_core.factions.mariners import Mariner
from ul_core.factions.fae import Faerie


class AudioMaster(DirectObject):
    def __init__(self):
        self.illegalMoveSound = loader.loadSfx('sounds/nope_bad.wav')
        self.clickSound = loader.loadSfx('assets/sounds/UI_generic1.wav')
        self.startFishSound = loader.loadSfx('assets/sounds/factionAbility_mariner01.wav')
        self.endFishSound = loader.loadSfx('assets/sounds/factionAbility_mariner02.wav')
        self.templarAbilitySound = loader.loadSfx('assets/sounds/factionAbility_templar.wav')
        self.thiefAbilitySound = loader.loadSfx('assets/sounds/factionAbility_thieves.wav')

        Templar.selectSound = loader.loadSfx('assets/sounds/select_templar.wav')
        Thief.selectSound = loader.loadSfx('assets/sounds/select_thieves.wav')
        Mariner.selectSound = loader.loadSfx('assets/sounds/select_mariner.wav')
        Faerie.selectSound = loader.loadSfx('assets/sounds/select_fey.wav')

        self.mulliganSound = loader.loadSfx('assets/sounds/mulligan_button.wav')
        self.mulliganSelectSound = loader.loadSfx('assets/sounds/mulligan_select.wav')
        self.mulliganDeselectSound = loader.loadSfx('assets/sounds/mulligan_unselect.wav')

    def playDecision(self):
        if isinstance(base.player, Mariner):
            self.endFishSound.play()
