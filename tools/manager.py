"""
testcanarybot bot manager [TPPM wrapper]
Copyright 2021 kensoi

works with projects that's has generated root.py file via TPPM
put this file into folder where you located all your projects. It shall look like this:

your_dir/
  manager.py <-- TPPM wrapper
  botName1/
    assets/
    library/
    root.py
  botName2/
    assets/
    library/
    root.py


$ python ./manager.py
"""

import subprocess

projects = ['botName1', 'botName2'] # list of projects by project folder name
subprocess.run(f'python -m testcanarybot --run {" ".join(projects)}'.split())