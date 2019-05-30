from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from panda3d.core import PointLight, AmbientLight, VBase4
from scenes.zoneMaker import ZoneMaker
import hud.game
from ul_core.factions import templars, mariners, thieves, fae
import hud.templarHud as templarHud
import hud.marinerHud as marinerHud
import hud.thiefHud as thiefHud
import hud.faerieHud as faerieHud


class Scene(DirectObject):
    def __init__(self, player):
        super().__init__()
        self.player = player

        # Set up the game UI
        if isinstance(self.player, templars.Templar):
            base.guiScene = templarHud.TemplarHud(base.gameState)
        elif isinstance(self.player, mariners.Mariner):
            base.guiScene = marinerHud.MarinerHud(base.gameState)
        elif isinstance(self.player, thieves.Thief):
            base.guiScene = thiefHud.ThiefHud(base.gameState)
        elif isinstance(self.player, fae.Faerie):
            base.guiScene = faerieHud.FaerieHud(base.gameState)
        else:
            base.guiScene = hud.game.GameHud(self.gameState)

        self.base_model = base.loader.loadModel('env.bam', noCache = True)
        self.base_model.reparentTo(base.render)
        # So it looks like there's an object called <BlenderRoot>
        # that gets loaded when you pull in a .blend file.
        # We need to search for the actual nodes we want in <BlenderRoot>
        self.model = self.base_model.find('<BlenderRoot>')
        base.camera.setPosHpr(self.model.find('Camera'), 0, 0, 0, 0, -90, 0)
        base.disableMouse()  # Fixes all your camera woes

        self.hept = self.model.find('Plane')
        self.hept.setTransparency(True)
        base.taskMgr.add(self.rotateTask, 'RotateHeptTask')

        # Convert the blender point light to a panda one
        #blenderLight = self.model.find('Point Light')
        #pandaLight = PointLight('Point Light')
        #pandaLight.setColor(VBase4(1, 1, 1, 1))
        #lightNode = blenderLight.attachNewNode(pandaLight)
        #base.render.setLight(lightNode)

        # Ambient lighting so we can easily see cards
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        alnp = base.render.attachNewNode(alight)
        base.render.setLight(alnp)

        spawn = self.model.find('Spawn')
        self.zoneMaker = ZoneMaker(
            self.player,
            self.model,
            playerHand=spawn.find('Player Hand'),
            enemyHand=spawn.find('Enemy Hand'),
            playerBoard=spawn.find('Player Board'),
            enemyBoard=spawn.find('Enemy Board'),
            playerFace=spawn.find('Player Face'),
            enemyFace=spawn.find('Enemy Face'),
            playerGraveyard=spawn.find('Player Graveyard'),
            enemyGraveyard=spawn.find('Enemy Graveyard'))

    def redraw(self):
        base.guiScene.redraw()
        self.zoneMaker.redrawAll()

    def rotateTask(self, task):
        if self.player.active:
            deltaTime = globalClock.getDt()
            self.hept.setHpr(self.hept, deltaTime * 5, 0, 0)
        return Task.cont

    def onKicked(self):
        """
        Called when the player is kicked from the game
        """
        base.guiScene.showBigMessage("Kicked")

    def unmake(self):
        base.guiScene.unmake()
        self.zoneMaker.unmake()
        self.base_model.removeNode()


if __name__ == '__main__':
    from direct.showbase.ShowBase import ShowBase
    from ul_core.core.game import Game
    from ul_core.factions.templars import Templar
    from panda3d.core import loadPrcFileData
    from hud.hud import Fonts

    loadPrcFileData('', 'model-path assets')

    class App(ShowBase):
        def __init__(self):
            super().__init__()
            self.game = Game(Templar, Templar)
            self.player, self.enemy = self.game.players
            self.game.start()
            self.active = True
            self.gameState = self.player  # Hack so we get active property
            self.fonts = Fonts()
            self.player.hasMulliganed = True
            self.bothPlayersMulliganed = True
            self.scene = Scene(self.player)
            self.scene.zoneMaker.redrawAll()

    app = App()
    app.run()
