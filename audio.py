from direct.showbase.DirectObject import DirectObject


class AudioMaster(DirectObject):
    def __init__(self):
        self.illegalMoveSound = loader.loadSfx('sounds/nope_bad.wav')
        self.clickSound = loader.loadSfx(
            'sounds/108317__robinhood76__02030-swooshing-punch.wav')

    def playIllegalMove(self):
        self.illegalMoveSound.play()