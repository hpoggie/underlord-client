from ul_core.net.enums import Zone


def cardToZie(player, card):
    """
    Convert a card to Zone, Index, Enemy representation
    """
    if card is None:
        return (-1, -1, 0)

    return (card.controller.zones.index(card.zone), card.zone.index(card),
            card.controller is player.opponent)


def playerFace():
    return (Zone.face, 0, False)


def enemyFace():
    return (Zone.face, 0, True)
