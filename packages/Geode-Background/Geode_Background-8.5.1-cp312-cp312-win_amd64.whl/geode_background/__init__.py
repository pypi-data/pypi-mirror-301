## Copyright (c) 2019 - 2024 Geode-solutions

import os, pathlib
os.add_dll_directory(pathlib.Path(__file__).parent.resolve().joinpath('bin'))

from .surface import *
from .solid import *
from .brep import *
