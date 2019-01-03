import ul_core.net.network as network
from . import state
from . import actions
from . import rpcReceiver


class Client:
    def __init__(self, ip, port, verbose):
        self.state = state.ClientState()
        self.rpcReceiver = rpcReceiver.RpcReceiver(
            self.state, None)
        self.networkManager = network.ClientNetworkManager(
            self.rpcReceiver, ip, port)
        self.networkManager.verbose = verbose
        self.clientActions = actions.ClientActions(
            self.state, self.networkManager)
        self.observer = None

    def add_observer(self, cb):
        self.observer = cb
        self.rpcReceiver.callbacks = cb

    def connect(self, addr):
        self.networkManager.connect(addr)
