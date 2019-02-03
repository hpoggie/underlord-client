import math


def fanHand(n):
    """
    Return a list of transforms for a fanned hand of n cards
    """
    scale = 2
    minPosX = -n / 2 / scale
    maxPosX = n / 2 / scale
    minRot = -45.0
    maxRot = -minRot

    if n < 4:
        step = (maxPosX - minPosX) / (n + 1)
        minPosX += step
        maxPosX -= step
        rotStep = (maxRot - minRot) / (n + 1)
        minRot += rotStep
        maxRot -= rotStep

    posX = minPosX
    posY = -1
    rot = minRot

    transforms = []

    for i in range(0, n):
        if maxPosX - minPosX > 0:
            curve = math.sin(
                (posX - minPosX) / (maxPosX - minPosX) * math.pi)
            posZ = 0.5 * curve - 2
        else:
            posZ = -2
        transforms.append((posX, posY, posZ, 0, 0, rot))
        if n > 1:
            posX += (maxPosX - minPosX) / (n - 1)
            posY -= 0.07
            rot += (maxRot - minRot) / (n - 1)

    return transforms
