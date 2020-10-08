import os

from .bot import TestCanaryBot

def getLibrary(file):
    return os.path.abspath(file)[:-len(file)] + '\\library\\'