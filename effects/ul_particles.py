import particles.vfx_loader
from panda3d.core import loadPrcFileData

def load_dust():
    dust = particles.vfx_loader.load('effects/dust/dust.json')
    dust.setScale(0.1, 0.1, 0.1)
    dust.setHpr(0, 0, 0)
    return dust
