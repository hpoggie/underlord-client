# Underlord

Underlord is an online ccg-esque game, currently in development.

# Running it

The easiest way to run the client is to grab it from the Releases page. If you
want to run it from source:

```
pip install -i https://archive.panda3d.org/ panda3d
pip install GitPython
git clone git@github.com:hpoggie/Underlord.git
cd underlord-client
python __main__.py
```

Underlord is written in python 3. I'm assuming you're running this inside
a virtualenv. If not, replace python with python3 and pip with pip3.

If you want to know how to use virtualenv, see
[here](https://virtualenv.pypa.io/en/stable/). I recommend using
virtualenvwrapper, which is explained
[here](https://virtualenvwrapper.readthedocs.io/en/latest/).
