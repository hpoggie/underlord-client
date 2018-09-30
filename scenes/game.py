from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from scenes.zoneMaker import ZoneMaker


class Scene(DirectObject):
    def __init__(self):
        super().__init__()
        self.model = base.loader.loadModel('env.bam')
        self.model.reparentTo(base.render)
        base.camera.setPosHpr(self.model.find('Camera'), 0, 0, 0, 0, -90, 0)
        base.disableMouse()  # Fixes all your camera woes

        self.hept = self.model.find('Plane')
        base.taskMgr.add(self.rotateTask, 'RotateHeptTask')

        spawn = self.model.find('Spawn')
        self.zoneMaker = ZoneMaker(
            self.model,
            playerHand=spawn.find('Player Hand'),
            enemyHand=spawn.find('Enemy Hand'),
            playerBoard=spawn.find('Player Board'),
            enemyBoard=spawn.find('Enemy Board'),
            playerFace=spawn.find('Player Face'),
            enemyFace=spawn.find('Enemy Face'),
            playerGraveyard=spawn.find('Player Graveyard'),
            enemyGraveyard=spawn.find('Enemy Graveyard'))

    def rotateTask(self, task):
        deltaTime = globalClock.getDt()
        self.hept.setHpr(self.hept, deltaTime * 5, 0, 0)
        return Task.cont

    def unmake(self):
        self.zoneMaker.unmake()
        self.model.removeNode()


if __name__ == '__main__':
    from direct.showbase.ShowBase import ShowBase
    from ul_core.core.game import Game
    from ul_core.factions.templars import Templar
    from panda3d.core import loadPrcFileData

    loadPrcFileData('', 'model-path assets')

    class App(ShowBase):
        def __init__(self):
            super().__init__()
            self.game = Game(Templar, Templar)
            self.player, self.enemy = self.game.players
            self.game.start()
            self.scene = Scene()
            self.hasMulliganed = True
            self.scene.zoneMaker.redrawAll()

    app = App()
    app.run()
