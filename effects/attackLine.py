from panda3d.core import MeshDrawer, Vec3, Vec4
from direct.showbase.DirectObject import DirectObject


class Line(DirectObject):
    """
    For drawing a line when picking target for attack
    """
    def __init__(self):
        self.meshDrawer = MeshDrawer()
        self.meshDrawer.setBudget(2)
        mdNode = self.meshDrawer.getRoot()
        mdNode.reparentTo(base.render)
        mdNode.setDepthWrite(False)
        mdNode.setTransparency(True)
        mdNode.setTwoSided(True)
        # mdNode.setTexture(loader.loadTexture("pixel.png"))
        mdNode.setBin("fixed", 0)
        mdNode.setLightOff(True)

    def draw(self, start, end):
        self.meshDrawer.begin(base.cam, render)
        self.meshDrawer.segment(
            Vec3(*start),
            Vec3(*end),
            frame=Vec4(0, 0, 1, 1),  # Use entire texture
            thickness=0.1,
            color=Vec4(0, 0, 0, 255))
        self.meshDrawer.end()

    def clear(self):
        self.meshDrawer.begin(base.cam, render)
        self.meshDrawer.end()
