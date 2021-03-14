import os
from .framework._application import (
    _app as app, 
    _codenameToINT as codenameToINT, 
    _correctCodeName as correctCodeName
    )


version_raw = {
    'sorted': {
        'stable': {},

        'unstable': {},

        'dev': {
            1: {0: [1, 2]}
        }
    },
    'root': {
        #convertedINT: currentCodeName
    }
}


for i in version_raw['sorted'].keys():
    for j in version_raw['sorted'][i].keys():
        for k in version_raw['sorted'][i][j].keys():
            for l in version_raw['sorted'][i][j][k]:
                version_raw['root'][codenameToINT(j,k,l)] = correctCodeName(j,k,l) + " " + i


version = version_raw['root'][max(version_raw['root'].keys())]


__version__ = version

__title__ = 'TestCanaryBot, ' + version
__author__ = 'Kensoi'
__license__ = 'Apache v2'
__copyright__ = 'Copyright 2021 Kensoi'

__doc__ = "kensoi/testcanarybot, " + version + """
Documentation is available at kensoi.github.io/testcanarybot
"""