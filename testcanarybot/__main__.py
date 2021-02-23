import argparse
import os
import typing

from .framework._values import parsename
from .framework._values import bool_str
from .framework._values import gen_str

module_clear = "from testcanarybot import objects\nfrom testcanarybot import exceptions #handling and raising errors\n\"\"\"\n(c) kensoi.github.io, since 2020\n\"\"\"\nclass Main(objects.libraryModule):\n\tasync def start(self, tools: objects.tools):\n\t\tpass # create task at start\n\n\t@objects.ContextManager(commands = [\"check\"])\n\tasync def ContextManagerHandler(self, tools: objects.tools, package: objects.package):\n\t\tawait tools.api.message.send(random_id = tools.random_id, peer_id = package.peer_id, message = \"handler is working!\")"

parser = argparse.ArgumentParser(
    description = """TestCanaryBot Pocket Manager. V2
    + creating standart folders
    + creating sampled plugin
    """
    )

parser.add_argument("-cf", dest="create_folder", action = 'store_true', help='create important folders with instructions')
parser.add_argument("-cm", dest="create_module", action = 'store_true', help='create module testcanarybot')
parser.add_argument("--name", type = str, default = "", help='module name on folder')
parser.add_argument("-f", dest = "folder", action = 'store_true', help='create module in a folder')

args = parser.parse_args()

if args.create_folder:
    print("Creating directories...")
    from .framework._application import _create_folders as create_folders
    create_folders()

    print("Creating readme files...")

    with open(os.getcwd() + '\\library\\readme.txt', 'w+') as readme:
        readme.write("(c) kensoi.github.io, since 2020\n=======create sampled module========\n\"python -m testcanarybot -cm [--name {module_name_without_space}] [-f]")
    with open(os.getcwd() + '\\assets\\readme.txt', 'w+') as readme:
        readme.write("(c) kensoi.github.io, since 2020\n================USAGE================\nfrom testcanarybot.assets import _assets\n\nassets = _assets()\n\nwith assets(\"readme.txt\", \"r+\") as readme:\n\tprint(readme.read())")
    
    print("Done! Look new files at created folders: ./assets/ and ./library/ ")

elif args.create_module:
    print('parsing module name...')
    name = parsename(args.name)

    if args.folder:
        print('creating module directory...')
        os.mkdir(os.getcwd() + '\\library\\' + name)
        name += '\\main.py'
    else:
        name += '.py'

    print('writing code example...')
    with open(os.getcwd() + '\\library\\' + name, 'w+') as module:
        module.write(module_clear)
    
    print('Done! Result ./library/' + name.replace('\\', '/'))

