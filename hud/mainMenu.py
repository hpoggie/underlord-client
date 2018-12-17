import textwrap
from panda3d.core import TextNode

from . import hud


commit_hash = ''


try:
    import git
    repo = git.Repo('.')
    # Get the hash of the latest commit
    commit_hash = repo.git.rev_parse('--short', 'HEAD')
except:  # If it doesn't work, don't worry about it
    pass


class MainMenu(hud.Scene):
    def __init__(self):
        super().__init__()

        main = self.root.attachNewNode('main')

        self.label(
            text="UNDERLORD",
            font=self.titleFont,
            scale=0.3,
            pos=(0, 0.4, 0),
            parent=main)

        if commit_hash != '':
            self.label(
                text='latest commit: ' + commit_hash,
                pos=(0, 0.3, 0),
                parent=main)

        base.numPlayersLabel = self.label(
            text="Getting server info...",
            pos=(0, 0.2, 0),
            mayChange=True,
            parent=main)

        self.credits = self.root.attachNewNode('credits')
        try:
            with open('CREDITS.txt') as f:
                self.creditsText = '\n'.join(  # Don't wrap line breaks
                    textwrap.fill(line, width=60)
                    for line in f.read().split('\n'))
        except OSError:
            self.creditsText = ''

        self.label(
            text=self.creditsText,
            align=TextNode.ALeft,
            scale=0.05,
            pos=(-0.7, 0.5, 0),
            parent=self.credits)

        self.credits.hide()

        def connect():
            base.connectionManager.startGame()

        def showCredits():
            main.hide()
            self.credits.show()

        def hideCredits():
            main.show()
            self.credits.hide()

        self.button(
            text="Back",
            pos=(0, 0, -0.7),
            parent=self.credits,
            command=hideCredits)

        def quit():
            base.userExit()

        buttons = (
            ("Play", connect),
            ("Credits", showCredits),
            ("Quit", quit))
        buttonPos = iter([
            (0, 0, len(buttons) * 0.15 - i * 0.15 - 0.5)
            for i in range(len(buttons))])
        for b in buttons:
            self.button(
                text=b[0],
                command=b[1],
                pos=next(buttonPos),
                frameSize=(-2, 2, -0.5, 1),
                parent=main)

    def showWaitMessage(self):
        self.label(
            text="Waiting for another player.",
            pos=(0, -0.5, 0))
