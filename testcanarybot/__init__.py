import os

from .bot import TestCanaryBot

def getPath(file):
    return os.path.abspath(file)[:-len(file)]