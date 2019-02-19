import particles.vfx_loader
from panda3d.core import loadPrcFileData

loadPrcFileData('', 'model-path assets/effects/dust')

def load_dust():
    return particles.vfx_loader.load('assets/effects/dust/dust.json')
