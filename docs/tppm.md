# TestCanaryBot Project Package Manager
```bash
python -m testcanarybot --create project_name [--token TOKEN] [--group GROUP] # create project

python -m testcanarybot --run project_name                     # init one project
python -m testcanarybot --run project_name1 project_name2      # init a few projects
python -m testcanarybot --run info                             # get information about callable directories
python -m testcanarybot --run all                              # run all directories from this catalogue

python -m testcanarybot --project project_name --cm module_name [-f] # create module (flag -f = create as folder with main.py file)
```


## Создание бота

```bash
$ python -m testcanarybot --create BotProjectDirName --token 7a6fa4dff77a228eeda56603b8f53806c883f011c40b72630bb50df056f6479e52a --group 123123
```
* **BotProjectDirName** - название директории, в которой будет создан чатбот
* **--token** - ваш токен (ключ доступа сообщества)
* **--group** - идентификатор сообщества, в котором будет работать бот

## Создание модуля с обработчиками


```bash
$ python -m testcanarybot --project BotProjectDirName --cm ModuleName [-f] [--library library]
tppm >> manager for << BotProjectDirName >>
tppm >> created folder << ModuleName >>
tppm >> Done! Results at ./BotProjectDirName/library/
```
* **BotProjectDirName** - название директории, в которой расположены данные чатбота
* **ModuleName** - название создаваемого модуля                              
* **-f**  - флаг: создать в **ModuleName**/main.py                    

## Способы запустить бота

#### Запуск в обход TPPM

```bash
$ python ./BotName1/root.py [--library library] [--assets assets]
tppm >> launching the project directly...
```

#### Для запуска нескольких проектов

```bash
$ python -m testcanarybot --run BotName1 BotName2 [--library library] [--assets assets]
tppm >> @bot1 initialised, started #BotName1 folder
tppm >> @bot2 initialised, started #BotName2 folder
```
P.S. можно использовать TPPM Wrapper.


#### Для запуска всех проектов в директории

```bash
$ python -m testcanarybot --run all [--library library] [--assets assets]
tppm >> @bot1 initialised, started #BotName1 folder
tppm >> @bot2 initialised, started #BotName2 folder
# i.e. all folders from current directory
```

#### Run info

Данная команда выдаст список директорий в рабочей папке (или в ```--path os.getcwd()```), которые testcanarybot будет воспринимать как проект бота

Фильтр обработки рабочей папки:

* наличие **root.py** (не папка)
* наличие **assets** (папка) (= --assets)
* наличие **library** (папка) (= --library)