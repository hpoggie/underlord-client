from setuptools import setup
import git

r = git.Repo('.')

setup(
    name="Underlord",
    version=str(r.tags[-1]),  # Most recent tag as version
    options={
        'build_apps': {
            'exclude_modules': [
                'GitPython'
            ],
            'include_patterns': [
                '**/*.png',
                '**/*.ttf',
                '**/*.bam',
                '**/*.blend',
                '**/*.wav',
                'CREDITS.txt'
            ],
            'plugins': [
                'pandagl',
                'p3openal_audio',
                'p3assimp',
            ],
            'gui_apps': {
                'Underlord': '__main__.py',
            },
        }
    },
)
