import ul_core.factions.thieves
from hud.game import GameHud
from panda3d.core import TextNode
from direct.gui.DirectGui import OnscreenText
# https://www.panda3d.org/manual/index.php/DirectEntry
from direct.gui.DirectGui import DirectEntry

from scenes.zoneMaker import hideCard, showCard


class ThiefHud(GameHud):
    def __init__(self, clientState):
        super().__init__(clientState)
        self.entryLabel = self.label(
            text='',
            mayChange=True)

        self.entry = DirectEntry(
            initialText='Type card name...',
            scale=0.05,
            focus=1,
            command=self.useThiefAbility,
            focusInCommand=lambda: self.entry.enterText(''))

        self.entry.hide()

        self.thiefAbilityButton = self.button(
            text="Faction Ability",
            scale=1,
            pos=(0, 0, -1),
            parent=self.endTurnButton,
            command=self.onThiefAbilityButton)

    def useThiefAbility(self, cardname):
        toDiscard = self.toDiscard.getPythonTag('card')
        toSteal = self.toSteal.getPythonTag('card')
        base.clientActions.useThiefAbility(
            toDiscard, toSteal, cardname)
        base.audioMaster.thiefAbilitySound.play()
        base.mouseHandler.targeting = False
        self.entry.hide()

    def onThiefAbilityButton(self):
        def chooseTarget(target):
            if target is None:
                base.mouseHandler.targeting = False
                showCard(self.toDiscard)
                return
            elif target.getPythonTag('zone') is not base.enemy.facedowns:
                return
            self.toSteal = target
            self.entry.show()

        def chooseDiscard(target):
            if target is None:
                base.mouseHandler.targeting = False
                return
            elif target.getPythonTag('zone') is not base.player.hand:
                return
            self.toDiscard = target
            hideCard(target)
            base.mouseHandler.startTargeting(
                "Choose a target.",
                chooseTarget)

        base.mouseHandler.startTargeting(
            "Choose a card to discard.",
            chooseDiscard)

    def redraw(self):
        super().redraw()

        # TODO: kludge
        if hasattr(self, 'thiefAbilityButton'):
            self.thiefAbilityButton.show()
