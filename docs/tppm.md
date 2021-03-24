#TPPM commands
```bash
python -m testcanarybot --create project_name [--token TOKEN] [--group GROUP] # create project

python -m testcanarybot --run project_name                     # init one project
python -m testcanarybot --run project_name1 project_name2      # init a few projects
python -m testcanarybot --run info                             # get information about callable directories
python -m testcanarybot --run all                              # run all directories from this catalogue

python -m testcanarybot --project project_name --cm module_name [-f] # create module (flag -f = create as folder with main.py file)
```