from direct.showbase.DirectObject import DirectObject


class ConnectionManager(DirectObject):
    """
    Handles the task of connecting to the server.
    """
    def __init__(self, addr, networkInstructions, scene):
        self.connectionUI = scene
        self.addr, self.networkInstructions = (addr, networkInstructions)

    def tryConnect(self):
        try:
            # connect to the remote server if no arg given
            self.connect()
            base.onConnectedToServer()
        except ConnectionRefusedError:
            self.connectionUI.showConnectionError(self.retryConnection)
            return

    def connect(self):
        base.client.connect(self.addr)

    def startGame(self):
        base.readyUp()

    def retryConnection(self):
        self.connectionUI.connectingLabel.show()
        self.tryConnect()
