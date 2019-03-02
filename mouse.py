from panda3d.core import CollisionNode, GeomNode, CollisionRay
from direct.showbase.DirectObject import DirectObject

from ul_core.core.exceptions import IllegalMoveError
import ul_core.core.card

import scenes.zoneMaker as zoneMaker
from effects import attackLine
import cardBuilder


# Adapted from the asteroids panda3d example
# This function, given a line (vector plus origin point) and a desired y value,
# will give us the point on the line where the desired y value is what we want.
# This is how we know where to position an object in 3D space based on a 2D mouse
# position. It also assumes that we are dragging in the XZ plane.
#
# This is derived from the mathematical of a plane, solved for a given point
def PointAtZ(z, point, vec):
    return point + vec * ((z - point.getZ()) / vec.getZ())


def inDropZone(pos):
    return pos.y > -6 and pos.y < 6


class MouseHandler (DirectObject):
    def __init__(self):
        self.accept('mouse1', self.onMouse1Down, [])  # Left click
        self.accept('mouse1-up', self.onMouse1Up, [])
        self.accept('mouse3', self.onMouse3Down, [])  # Right click

        self.showCollisions = False

        pickerNode = CollisionNode('mouseRay')
        pickerNP = camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(cardBuilder.cardCollisionMask)
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        base.cTrav.addCollider(pickerNP, base.handler)
        if self.showCollisions:
            base.cTrav.showCollisions(render)
        base.disableMouse()

        self.activeCard = None
        self._targeting = False

        self._dragging = None

        # Counts down between clicks to detect double click
        self.doubleClickTimer = -1.0
        self.doubleClickInterval = 1.0

        self.line = attackLine.Line()

    @property
    def targeting(self):
        return self._targeting

    @targeting.setter
    def targeting(self, value):
        self._targeting = value
        if self._targeting:
            base.guiScene.showTargeting()
        else:
            base.guiScene.hideTargeting()

    def startTargeting(self, targetDesc, callback=None):
        base.targetDesc = targetDesc
        self.targeting = True
        if callback is not None:
            base.targetCallback = callback

    def getObjectClickedOn(self):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

            base.cTrav.traverse(render)
            if (base.handler.getNumEntries() > 0):
                base.handler.sortEntries()
                pickedObj = base.handler.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetPythonTag('zone')
                if pickedObj == self.dragging and base.handler.getNumEntries() > 1:
                    pickedObj = base.handler.getEntry(1).getIntoNodePath()
                    pickedObj = pickedObj.findNetPythonTag('zone')

                return pickedObj

    def doClick(self):
        pickedObj = self.getObjectClickedOn()

        if self.dragging:
            return

        if self.targeting and pickedObj is not None:
            base.targetCallback(pickedObj)
        elif pickedObj and not pickedObj.isEmpty():
            zone = pickedObj.getPythonTag('zone')
            if zone is base.player.hand and not base.gameState.hasMulliganed:
                c = pickedObj.getPythonTag('card')
                if c in base.toMulligan:
                    base.toMulligan.remove(c)
                else:
                    base.toMulligan.append(c)
                base.zoneMaker.makeMulliganHand()
            elif zone is base.player.hand:
                self.dragging = pickedObj
            elif zone is base.player.facedowns:
                c = pickedObj.getPythonTag('card')
                if self.activeCard:
                    self.activeCard = None
                elif c.requiresTarget:
                    self.startTargeting(c.targetDesc)
                    def callback(target):
                        base.revealFacedown(pickedObj, target)
                        base.finishTargeting()
                    base.targetCallback = callback
                else:
                    base.revealFacedown(pickedObj)
            elif zone is base.player.faceups:
                c = pickedObj.getPythonTag('card')
                if not c.hasAttacked:
                    self.activeCard = pickedObj
            elif zone is base.enemy.facedowns and self.activeCard:
                base.attack(self.activeCard, pickedObj)
                self.activeCard = None
            elif zone == base.enemy.faceups and self.activeCard:
                base.attack(self.activeCard, pickedObj)
                self.activeCard = None
            elif zone is base.enemy.face and self.activeCard:
                base.attack(self.activeCard, pickedObj)
                self.activeCard = None
        else:
            self.activeCard = None

    @property
    def dragging(self):
        return self._dragging

    @dragging.setter
    def dragging(self, obj):
        if obj is None:
            self._dragging.removeNode()
            base.zoneMaker.makePlayerHand()  # Put the card back
        else:
            obj.reparentTo(base.zoneMaker.scene)
            obj.setHpr(0, -90, 0)

        self._dragging = obj

    def stopDragging(self):
        """
        Stop dragging the card and play it if it's in the drop zone
        """
        # Borders of the drop zone
        # If you drop the card outside the drop zone,
        # the action is cancelled
        pos = self._dragging.getPos()
        if inDropZone(pos):
            try:
                target = None
                c = self.dragging.getPythonTag('card')
                if c.fast:
                    pickedObj = self.getObjectClickedOn()
                    if pickedObj is not None and pickedObj != self.dragging:
                        target = pickedObj
                    elif c.requiresTarget:
                        # don't fizzle if no valid target
                        self.dragging = None
                        return

                base.playCard(self._dragging, target)
            except IllegalMoveError as e:
                print(e)
        self.dragging = None

    def onMouse1Down(self):
        if self._dragging is not None:
            self.stopDragging()
            self.doubleClickTimer = -1
        elif self.doubleClickTimer <= 0:
            self.doubleClickTimer = 0.2
            try:
                self.doClick()
            except IllegalMoveError as e:
                print(e)

    def onMouse1Up(self):
        if self._dragging and self.doubleClickTimer <= 0:
            self.stopDragging()

    def onMouse3Down(self):
        if self.targeting:
            base.targetCallback(None)

        if self.dragging:
            self.dragging = None

    def mouseToXYPlane(self):
        mpos = base.mouseWatcherNode.getMouse()
        # See the Panda3d chess example
        self.pickerRay.setFromLens(
            base.camNode, mpos.getX(), mpos.getY())
        # Get a vector relative to the camera position
        nearPoint = render.getRelativePoint(
            camera, self.pickerRay.getOrigin())
        nearVec = render.getRelativeVector(
            camera, self.pickerRay.getDirection())

        return PointAtZ(.5, nearPoint, nearVec)

    def mouseOverTask(self):
        if base.mouseWatcherNode.hasMouse():
            if self.doubleClickTimer > 0:
                # Count down based on how long it took to draw the last frame
                self.doubleClickTimer -= globalClock.getDt()

            if hasattr(self, '_activeObj') and self._activeObj is not None:
                zone = self._activeObj.getPythonTag('card').zone
                if zone is base.player.facedowns or zone is base.enemy.facedowns:
                    zoneMaker.hideCard(self._activeObj)

                base.zoneMaker.unfocusCard()
                self._activeObj = None

            if self.dragging is not None:
                # Drag the card in the XY plane
                self.dragging.setPos(self.mouseToXYPlane())
            elif base.gameState.hasMulliganed:
                pickedObj = self.getObjectClickedOn()
                if pickedObj:
                    card = pickedObj.getPythonTag('card')
                    if card is not None and not pickedObj.getPythonTag('disableFocus'):
                        self._activeObj = pickedObj
                        if card.zone in (
                                base.enemy.hand,
                                base.player.facedowns,
                                base.enemy.facedowns):
                            zoneMaker.showCard(pickedObj)
                        base.zoneMaker.focusCard(pickedObj)

                if self.activeCard:
                    basePos = (pickedObj.getPos(base.render)
                        if pickedObj is not None and not pickedObj.isEmpty()
                        else self.mouseToXYPlane()),
                    self.line.draw(
                        start=self.activeCard.getPos(base.render),
                        end=basePos)
                else:
                    self.line.clear()
