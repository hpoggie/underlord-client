import particles.vfx_loader
from panda3d.core import loadPrcFileData

def load_dust():
    return particles.vfx_loader.load('effects/dust/dust.json')
