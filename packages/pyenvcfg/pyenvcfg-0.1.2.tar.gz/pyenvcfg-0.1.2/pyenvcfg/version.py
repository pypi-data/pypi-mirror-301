#!/usr/bin/env python

"""Version module for pyenvcfg"""

import importlib.metadata

import toml

try:
    __version__ = importlib.metadata.version('pyenvcfg')
except:
    # Read version from pyproject.toml
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        pyproject = toml.load(f)
        __version__ = pyproject["tool"]["poetry"]["version"]