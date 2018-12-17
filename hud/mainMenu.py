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

        credits = self.text_screen('CREDITS.txt')
        showCredits = self.show_hide_screen(main, credits)

        howToPlay = self.text_screen('HOW_TO_PLAY.txt', textPos=(-0.7, 0.75, 0))
        showHowToPlay = self.show_hide_screen(main, howToPlay)

        def connect():
            base.connectionManager.startGame()

        def quit():
            base.userExit()

        buttons = (
            ("Play", connect),
            ("Credits", showCredits),
            ("How to Play", showHowToPlay),
            ("Quit", quit))
        buttonPos = iter([
            (0, 0, len(buttons) * 0.15 - i * 0.15 - 0.6)
            for i in range(len(buttons))])
        for b in buttons:
            self.button(
                text=b[0],
                command=b[1],
                pos=next(buttonPos),
                frameSize=(-3, 3, -0.5, 1),
                parent=main)

    def text_screen(self, filename, textPos=(-0.7, 0.5, 0)):
        node = self.root.attachNewNode('text_screen')

        try:
            with open(filename) as f:
                text = '\n'.join(  # Don't wrap line breaks
                    textwrap.fill(line, width=60)
                    for line in f.read().split('\n'))
        except OSError:
            text = ''

        self.label(
            text=text,
            align=TextNode.ALeft,
            scale=0.05,
            pos=textPos,
            parent=node)

        node.hide()
        return node

    def show_hide_screen(self, main, node, buttonPos=(0, 0, -0.9)):
        def show_screen():
            main.hide()
            node.show()

        def hide_screen():
            main.show()
            node.hide()

        self.button(
            text="Back",
            pos=buttonPos,
            parent=node,
            command=hide_screen)

        return show_screen

    def showWaitMessage(self):
        self.label(
            text="Waiting for another player.",
            pos=(0, -0.65, 0))
