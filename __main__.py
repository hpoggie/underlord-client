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
from ul_core.net.network import ClientNetworkManager
from ul_core.core.game import Phase
from ul_core.core.exceptions import IllegalMoveError
import ul_core.core.card
import ul_core.factions
from ul_core.factions import templars, mariners, thieves, fae
from mouse import MouseHandler
import hud
import hud.goingFirstDecision as gfd
import hud.mainMenu as mainMenu
import hud.factionSelect as factionSelect
from connectionManager import ConnectionManager
import networkInstructions
import hud.templarHud as templarHud
import hud.marinerHud as marinerHud
import hud.thiefHud as thiefHud
import hud.faerieHud as faerieHud
import protocol.actions
import protocol.state
import protocol.rpcReceiver

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

        # View the cards at an angle
        self.camera.setPosHpr(4, -15, -15, 0, 45, 0)

        # Set up the NetworkManager
        self.gameState = protocol.state.ClientState()
        instr = networkInstructions.NetworkInstructions(self)
        self.rpcReceiver = protocol.rpcReceiver.RpcReceiver(self.gameState, instr)
        self.networkManager = ClientNetworkManager(self.rpcReceiver, ip, port)
        self.networkManager.verbose = verbose
        self.clientActions = protocol.actions.ClientActions(
            self.gameState, self.networkManager)

        # Connect to the server
        self.connectionManager = ConnectionManager((ip, port), self)
        self.connectionManager.tryConnect()
        self.taskMgr.add(self.networkUpdateTask, "NetworkUpdateTask")

        self.availableFactions = ul_core.factions.availableFactions

        self.ready = False

    def onConnectedToServer(self):
        self.guiScene = mainMenu.MainMenu()

    @property
    def hasMulliganed(self):
        if self.gameState is None:
            return False
        else:
            return self.gameState.hasMulliganed

    @hasMulliganed.setter
    def hasMulliganed(self, value):
        self.gameState.hasMulliganed = value

    @property
    def active(self):
        if self.gameState is None:
            return False
        else:
            return self.gameState.active

    @active.setter
    def active(self, value):
        self.gameState.active = value

    @property
    def game(self):
        return self.gameState.game

    @property
    def guiScene(self):
        return self._guiScene

    @guiScene.setter
    def guiScene(self, value):
        """
        Used to control which menu is being shown
        """
        if hasattr(self, '_guiScene') and self._guiScene:  # TODO: kludge
            self._guiScene.unmake()
        self._guiScene = value

    def readyUp(self):
        """
        We are ready to play a game.
        """
        if not self.ready:
            self.networkManager.addPlayer()
            self.guiScene.showWaitMessage()
            self.ready = True

    def onEnteredGame(self):
        self.guiScene = factionSelect.FactionSelect()

    def pickFaction(self, index):
        """
        Tell the server we've picked a faction and are ready to start the game.
        """
        self.networkManager.selectFaction(index)
        self.gameState.faction = self.availableFactions[index]

        # Tell the user we're waiting for opponent
        self.guiScene.showWaitMessage()

    def goFirst(self):
        base.networkManager.decideWhetherToGoFirst(1)
        self.gameState.onGameStarted(goingFirst=True)
        self.onGameStarted(goingFirst=True)

    def goSecond(self):
        base.networkManager.decideWhetherToGoFirst(0)
        self.gameState.onGameStarted(goingFirst=False)
        self.onGameStarted(goingFirst=False)

    def onGameStarted(self, goingFirst=True):
        self.bothPlayersMulliganed = False
        self.toMulligan = []

        # Set up the game UI
        if isinstance(self.player, templars.Templar):
            self.guiScene = templarHud.TemplarHud()
        elif isinstance(self.player, mariners.Mariner):
            self.guiScene = marinerHud.MarinerHud()
        elif isinstance(self.player, thieves.Thief):
            self.guiScene = thiefHud.ThiefHud()
        elif isinstance(self.player, fae.Faerie):
            self.guiScene = faerieHud.FaerieHud()
        else:
            self.guiScene = hud.game.GameHud()
        self.gameScene = game.Scene()
        self.zoneMaker = self.gameScene.zoneMaker

        self.hasFirstPlayerPenalty = goingFirst

    def decideWhetherToGoFirst(self):
        self.guiScene = gfd.GoingFirstDecision()

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

    def mulligan(self):
        if not self.hasMulliganed:
            indices = [self.player.hand.index(c) for c in self.toMulligan]
            self.networkManager.mulligan(*indices)
            self.hasMulliganed = True
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
        If it's our reveal phase and the card is fast, play it face-up,
        otherwise play it face-down.
        """
        c = card.getPythonTag('card')
        t = self.nodeToGameEntity(target)

        if self.phase == Phase.reveal:
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

    def endPhase(self, *args, **kwargs):
        def entityOrBool(arg):
            return arg if isinstance(arg, bool) else self.nodeToGameEntity(arg)

        args = [entityOrBool(arg) for arg in args]
        kwargs = [entityOrBool(arg) for key, arg in kwargs.items()]

        self.clientActions.endPhase(args + kwargs)
        self.hasFirstPlayerPenalty = False

    def replace(self, nodes):
        cards = [self.nodeToGameEntity(node) for node in nodes]
        self.clientActions.replace(cards)

        for node in nodes:
            # Do getParent.getParent because of pivots
            # TODO: make this cleaner
            # NEVER COMPARE NODE PATHS w/ is. It seems to always return False
            if (node is not None and
                    node.getParent().getParent() == self.zoneMaker.playerHand):
                node.removeNode()

    def redraw(self):
        self.player.fishing = False
        self.zoneMaker.redrawAll()
        if self.mouseHandler.targeting:
            self.mouseHandler.targeting = False
        self.guiScene.redraw()

    def quitToMainMenu(self):
        self.taskMgr.doMethodLater(
            1, self._quitToMainMenuTask, "QuitToMainMenu")

    def _quitToMainMenuTask(self, task):
        if hasattr(self, 'gameScene'):  # TODO: kludge
            self.gameScene.unmake()
        self.guiScene = mainMenu.MainMenu()
        self.networkManager.requestNumPlayers()
        self.ready = False
        return Task.done

    def inputTask(self, task):
        try:
            self.mouseHandler.mouseOverTask()
        except IllegalMoveError as e:
            print(e)

        return Task.cont

    def networkUpdateTask(self, task):
        try:
            self.networkManager.recv()
        except ConnectionClosed:
            return Task.done

        return Task.cont


# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', action='store_true')
parser.add_argument('-a', type=str, default='174.138.119.84')
parser.add_argument('-p', type=int, default=9099)
args = parser.parse_args()

app = App(args.a, args.p, args.v)
app.run()
