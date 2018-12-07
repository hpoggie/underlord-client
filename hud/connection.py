from . import hud


class ConnectionUI(hud.Scene):
    def __init__(self):
        super().__init__()
        self.connectingLabel = self.label(text="connecting to server")

    def showConnectionError(self, callback):
        self.connectingLabel.hide()
        self.connectionFailedLabel = self.label(
            text="Error. Could not connect to server")
        self.reconnectButton = self.button(
            pos=(0, 0, -0.25),
            image="./reconnect.png",
            relief=None,
            command=callback)
