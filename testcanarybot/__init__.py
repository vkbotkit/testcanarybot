from . import packaet
from .packaet import app, message, testcanarybot_name_data
from .framework._library import join
import os


def root_init(name: str, file) -> bool:
    if name != "__main__":
        return False

    elif os.path.abspath(file) == os.getcwd():
        pass

    else:
        test = file[:file.rfind(join) + 1]
        os.chdir(test)

    message("launching the project directly...")

    return True

__version__ = testcanarybot_name_data['keywords']['version']

__title__ = testcanarybot_name_data['sep'].join([i for i in testcanarybot_name_data['keywords'].values() if i.lower() != 'stable'])
__author__ = 'Kensoi'
__license__ = 'Apache v2'
__copyright__ = 'Copyright 2021 kensoi'

__doc__ = "kensoi/testcanarybot, " + __version__ + """
Documentation is available at kensoi.github.io/testcanarybot
"""

__all__ = ['version', 'app', 'root_init']