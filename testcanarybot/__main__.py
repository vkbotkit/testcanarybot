description = """
testcanarybot project package manager;
Copyright 2021 kensoi
"""

import argparse
import importlib
import os
import sys
import time

from .framework._library import join
from .packaet import *

packaet_parser = argparse.ArgumentParser(description = description)

packaet_parser.add_argument("--path", type = str, default = os.getcwd(), help='[OPTIONAL] workspace path')

packaet_parser.add_argument("--run", type = str, default = [], nargs='+', help='run a list/run all/get info of projects')
packaet_parser.add_argument("--create", type = str, default = "", help='Create project')
packaet_parser.add_argument("--project",type = str, default = "", help='setting project')

packaet_parser.add_argument("--assets", type = str, default = "assets", help='[OPTIONAL] assets directory')
packaet_parser.add_argument("--library", type = str, default = "library", help='[OPTIONAL] library directory')

packaet_parser.add_argument("--token", type = str, default = "REQUIRED_TO_FILL!", help='[CREATE] community access token')
packaet_parser.add_argument("--service", type = str, default = "", help='[CREATE] community access token [optional]')
packaet_parser.add_argument("--group", type = str, default = "REQUIRED_TO_FILL!", help='[CREATE] community identificator')

packaet_parser.add_argument("--cm", type = str, default = "", help='[PROJECT] create module testcanarybot')
packaet_parser.add_argument("-f", dest = "folder", action = 'store_true', help='[PROJECT] create module in a folder')

args = packaet_parser.parse_args()

packaet_project_directory =  args.create + args.project
packaet_project_assets = args.assets
packaet_project_library = args.library
workingProjects = []

projects = os.listdir(args.path + join)

if packaet_project_directory == '' and args.run == []:
    message('Try to run command \"python testcanarybot -h\"')
    quit()

elif packaet_project_directory not in [args.create, args.project] and args.run == []:
    raise RuntimeError('2 or more args! \nTry to run command \"python testcanarybot -h\"')

if len(args.run) > 0:
    sys.path.append(args.path + join)

    if args.run in [['info'], ['all']]:
        if args.run[0] == 'info':
            message('Projects at this directory:\n\t- ' + '\n\t- '.join(getProjects(args.path)))

        elif args.run[0] == 'all':
            for i in getProjects(args.path):
                testApp = importlib.import_module(i + '.root')
                testBot = threadBot(testApp, i, packaet_project_assets, packaet_project_library, args.path)
                workingProjects.append(testBot)
                time.sleep(1)

    else:
        for i in args.run:
            if i in getProjects(args.path):
                testApp = importlib.import_module(i + '.root')
                testBot = threadBot(testApp, i, packaet_project_assets, packaet_project_library, args.path + join + i)
                workingProjects.append(testBot)
                time.sleep(1)
            else:
                raise ValueError(f"Directory does not exist or is not a bot project. Run \"python testcanarybot --create {i}\" to create project, and try again")

    while True:
        for bot in range(len(workingProjects)):
            if not workingProjects[bot].is_alive():
                workingProjects.pop(bot)

        if len(workingProjects) == 0:
            quit()
        time.sleep(3)


elif args.create != '':
    message('Creating project <<', packaet_project_directory, '>>')
    
    if packaet_project_directory not in projects:
        message("Creating directories")

        os.mkdir(args.path + join + packaet_project_directory)
        os.mkdir(args.path + join + packaet_project_directory + join + packaet_project_assets)
        os.mkdir(args.path + join + packaet_project_directory + join + packaet_project_library)

        message("Creating << root >>")

        with open(args.path + join + packaet_project_directory + join + 'root.py', 'w+') as root:
            root.write(packaet_root_raw.format(token = args.token, group = args.group, service_token = args.service))

        message("Creating << readme >>")

        with open(args.path + join + packaet_project_directory + join + packaet_project_library + join + 'readme.txt', 'w+') as readme:
            readme.write(packaet_readme_library.format(packaet_project_directory = packaet_project_directory))
        
        with open(args.path + join + packaet_project_directory + join + packaet_project_assets + join + 'readme.txt', 'w+') as readme:
            readme.write(packaet_readme_assets)
        message(f"Done! \n\tDirectory: ./{packaet_project_directory}/ \n\tUsage: python testcanarybot --run {packaet_project_directory}")
    
    else:
        raise RuntimeError("Folder exists! Try another name")

elif args.project != '':
    message("manager for <<", packaet_project_directory, ">>")

    if args.cm != '':
        packaet_module_name = parsename(args.cm) # if args.cm != '' else 'handler_' + gen_str(15)
        packaet_module_inFolder = args.folder

        if packaet_module_inFolder:
            if packaet_module_name not in os.listdir(args.path + join + packaet_project_directory + join + 'library' + join):
                os.mkdir(args.path + join + packaet_project_directory + join + 'library' + join + packaet_module_name)
            
            message("created folder <<", packaet_module_name, ">>")
            
            with open(args.path + join + packaet_project_directory + join + 'library' + join + packaet_module_name + "\\main.py", 'w+') as module:
                module.write(libraryModuleRaw)
            
            message("Done! Results at ./" + packaet_project_directory + "/library/")

        else:
            message("created file <<", packaet_module_name, ">>")
            
            with open(args.path + join + packaet_project_directory + join + 'library' + join + packaet_module_name + ".py", 'w+') as module:
                module.write(libraryModuleRaw)
            
            message("Done! Results at ./" + packaet_project_directory + "/library/")