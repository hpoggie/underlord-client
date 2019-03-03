"""
This is the client script. It takes game data and draws it on the screen.
It also takes user input and turns it into game actions.
"""

import argparse

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerQueue
from panda3d.core import loadPrcFileData
from direct.task import Task

from ul_core.net.network_manager import ConnectionClosed
from ul_core.core.exceptions import IllegalMoveError
import ul_core.factions
from mouse import MouseHandler
import hud
import hud.goingFirstDecision as gfd
import hud.mainMenu as mainMenu
import hud.factionSelect as factionSelect
import hud.connection
from connectionManager import ConnectionManager
import networkInstructions
import protocol.client

import scenes.game as game

loadPrcFileData(
    "",
    """
    win-size 500 500
    window-title Underlord
    fullscreen 0
    model-path assets
    """)


class App (ShowBase):
    def __init__(self, ip, port, verbose=False):
        super().__init__()

        # Set up mouse input
        base.cTrav = CollisionTraverser()
        self.handler = CollisionHandlerQueue()
        self.mouseHandler = MouseHandler()
        self.taskMgr.add(self.inputTask, "InputTask")

        # Set up the UI
        self.fonts = hud.hud.Fonts()
        self._scene = None

        # Set up the NetworkManager
        self.client = protocol.client.Client(ip, port, verbose)
        instr = networkInstructions.NetworkInstructions(self)
        self.client.add_observer(instr)

        self.clientActions = self.client.clientActions
        self.gameState = self.client.state

        # Connect to the server
        self.scene = hud.connection.ConnectionUI()
        self.connectionManager = ConnectionManager((ip, port), self, self.scene)
        self.connectionManager.tryConnect()
        self.taskMgr.add(self.networkUpdateTask, "NetworkUpdateTask")

    def onConnectedToServer(self):
        self.scene = mainMenu.MainMenu()

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        if self._scene:
            self._scene.unmake()
        self._scene = value

    def readyUp(self):
        """
        We are ready to play a game.
        """
        if not self.gameState.ready:
            self.clientActions.readyUp()
            self.scene.showWaitMessage()

    def onEnteredGame(self):
        self.scene = factionSelect.FactionSelect(
            ul_core.factions.availableFactions)

    def pickFaction(self, index):
        """
        Tell the server we've picked a faction and are ready to start the game.
        """
        self.clientActions.pickFaction(index)

        # Tell the user we're waiting for opponent
        self.scene.showWaitMessage()

    def goFirst(self):
        self.clientActions.goFirst()
        self.onGameStarted(goingFirst=True)

    def goSecond(self):
        self.clientActions.goSecond()
        self.onGameStarted(goingFirst=False)

    def onGameStarted(self, goingFirst=True):
        self.toMulligan = []

        self.scene = game.Scene(self.gameState.player)
        self.zoneMaker = self.scene.zoneMaker

        self.hasFirstPlayerPenalty = goingFirst

    def decideWhetherToGoFirst(self):
        self.scene = gfd.GoingFirstDecision()

    @property
    def player(self):
        return self.gameState.player

    @property
    def enemy(self):
        return self.gameState.enemy

    @property
    def phase(self):
        return self.gameState.game.phase

    @phase.setter
    def phase(self, value):
        self.gameState.game.phase = value

    @property
    def bothPlayersMulliganed(self):
        pls = self.gameState.game.players
        return pls[0].hasMulliganed and pls[1].hasMulliganed

    def mulligan(self):
        if not self.gameState.hasMulliganed:
            self.clientActions.mulligan(self.toMulligan)
            self.toMulligan = []  # These get GC'd
        else:
            print("Already mulliganed.")

    def nodeToGameEntity(self, node):
        if node is None:
            return None
        elif node.getPythonTag('zone') is self.player.face:
            return self.player.face
        elif node.getPythonTag('zone') is self.enemy.face:
            return self.enemy.face
        else:
            return node.getPythonTag('card')

    def finishTargeting(self):
        self.targetCallback = None
        self.activeDecision = None
        self.mouseHandler.targeting = False
        self.guiScene.hideTargeting()

    def playCard(self, card, target=None):
        """
        If the card is fast, play it face-up,
        otherwise play it face-down.
        """
        c = card.getPythonTag('card')
        t = self.nodeToGameEntity(target)

        if c.fast:
            if c.requiresTarget:
                self.clientActions.playFaceup(c, t)
            else:
                self.clientActions.playFaceup(c)
        else:
            self.clientActions.playFacedown(c)

    def revealFacedown(self, card, target=None):
        card = card.getPythonTag('card')
        target = self.nodeToGameEntity(target)

        self.clientActions.revealFacedown(card, target)

    def attack(self, card, target):
        self.clientActions.attack(
            card.getPythonTag('card'), self.nodeToGameEntity(target))

    def endTurn(self, *args, **kwargs):
        def entityOrBool(arg):
            return arg if isinstance(arg, bool) else self.nodeToGameEntity(arg)

        args = [entityOrBool(arg) for arg in args]
        kwargs = [entityOrBool(arg) for key, arg in kwargs.items()]

        self.clientActions.endTurn(args + kwargs)
        self.hasFirstPlayerPenalty = False

    def useTemplarAbility(self, target):
        self.clientActions.useTemplarAbility(self.nodeToGameEntity(target))
    
    def useMarinerAbility(self):
        self.clientActions.useMarinerAbility()

    def makeDecision(self, nodes):
        cards = [self.nodeToGameEntity(node) for node in nodes]
        self.clientActions.makeDecision(cards)

        for node in nodes:
            # NEVER COMPARE NODE PATHS w/ is. It seems to always return False
            if (node is not None and
                    node.getParent() == self.zoneMaker.playerHand):
                node.removeNode()

    def redraw(self):
        if self.mouseHandler.targeting:
            self.mouseHandler.targeting = False
        self.scene.redraw()

    def quitToMainMenu(self):
        self.taskMgr.doMethodLater(
            1, self._quitToMainMenuTask, "QuitToMainMenu")

    def _quitToMainMenuTask(self, task):
        self.scene = mainMenu.MainMenu()
        self.clientActions.requestNumPlayers()
        return Task.done

    def inputTask(self, task):
        try:
            self.mouseHandler.mouseOverTask()
        except IllegalMoveError as e:
            print(e)

        return Task.cont

    def networkUpdateTask(self, task):
        try:
            self.client.networkManager.recv()
        except ConnectionClosed:
            return Task.done

        return Task.cont


# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', action='store_true')
parser.add_argument('-a', type=str, default='174.138.119.84')
parser.add_argument('-p', type=int, default=9099)
parser.add_argument('--testing', '-t', action='store_true')
args = parser.parse_args()

if args.testing:
    args.a = '174.138.110.117'

app = App(args.a, args.p, args.v)
app.run()
