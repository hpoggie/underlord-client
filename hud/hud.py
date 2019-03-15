from panda3d.core import TransparencyAttrib
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage


class Fonts(DirectObject):
    def __init__(self):
        self.titleFont = loader.loadFont("fonts/Cinzel-Regular.ttf")
        self.bodyFont = loader.loadFont("fonts/Ubuntu-Regular.ttf")
        self.titleFont.setPixelsPerUnit(120)
        self.bodyFont.setPixelsPerUnit(60)


class Scene(DirectObject):
    def __init__(self):
        self.titleFont = base.fonts.titleFont
        self.bodyFont = base.fonts.bodyFont

        # Put everything under one node to make it easy to destroy
        self.root = base.aspect2d.attachNewNode(name="GuiScene")

        self.clickSound = base.loader.loadSfx(
            'sounds/108317__robinhood76__02030-swooshing-punch.wav')

    def label(self, **kwargs):
        defaultArgs = {}
        # Attach the label to the root.
        # Note that this does not affect pos/scale for OnscreenText
        defaultArgs['parent'] = self.root
        defaultArgs['font'] = self.bodyFont  # Use the default font
        defaultArgs['scale'] = 0.1
        kwargs = {**defaultArgs, **kwargs}  # Merge the 2 dicts; prefer kwargs
        return OnscreenText(**kwargs)

    def button(self, **kwargs):
        defaultArgs = {}
        # Attach the label to the root.
        # Note that this does not affect pos/scale for OnscreenText
        defaultArgs['parent'] = self.root
        defaultArgs['text_font'] = self.bodyFont  # Use the default font
        defaultArgs['scale'] = 0.1
        defaultArgs['clickSound'] = self.clickSound
        kwargs = {**defaultArgs, **kwargs}  # Merge the 2 dicts; prefer kwargs
        return DirectButton(**kwargs)

    def image(self, **kwargs):
        defaultArgs = {}
        defaultArgs['parent'] = self.root
        defaultArgs['scale'] = 0.1
        kwargs = {**defaultArgs, **kwargs}
        image = OnscreenImage(**kwargs)
        image.setTransparency(TransparencyAttrib.MAlpha)  # Enable alpha
        return image

    def unmake(self):
        self.root.detachNode()

    def showBigMessage(self, message):
        """
        Put huge text on the screen that obscures stuff
        """
        if hasattr(base, 'zoneMaker'):
            base.zoneMaker.mulliganHand.hide()
        self.label(
            text=message,
            scale=(0.5, 0.5, 0.5))
