import six
import os
import importlib

group_id = 0
group_mention = ''

class plugins_autoimport():
    __slots__ = ('name', 'method', 'all')
    def __init__(self, method = None):
        self.method = method
        self.name = method


    def __getattr__(self, method):
        self.name = (self.method + '.' if self.method else '') + method
        return lib_plugins(self.name)


    def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)
        try:
            test = getattr(
                importlib.import_module(
                        "library."+ (self.name[0:self.name.rfind('.')]) + ".main"
                    ), 
                self.name[self.name.rfind('.')+1:]
            )(kwargs)

        except Exception as e:
            print(e)

class plugins():
    def __init__(self, v, assets, api):
        self.v = v
        self.all = [i for i in self.getPlugins() if i != 'tools']
        self.plugins = self.upload(self.all)
        self.assets = assets
        self.api = api


    def getPlugins(self):
        try:
            return os.listdir(os.path.abspath(os.path.dirname(__file__)) + '\\lib\\')
        except Exception as e:
            print(e)
        

    def upload(self, all):
        pl = {}

        for plugin in all:
            if plugin != 'tools':
                try:
                    pluginObj = getattr(importlib.import_module("lib." + plugin + ".main"), 'lib_plugin')()
                except:
                    print(f"{plugin} повреждён")

                    self.all = [i for i in self.all if i != plugin]
                    continue

                if pluginObj.v == self.v:
                    if hasattr(pluginObj, 'name'):
                        if hasattr(pluginObj, 'update'):
                            pl[plugin] = pluginObj
                            print(f"{pluginObj.name} загружен")
                        else:
                            print(f"{pluginObj.name} не имеет аттрибута 'update'")
                            self.all = [i for i in self.all if i != plugin]
                    else:
                        print(f"{plugin} не имеет имени")
                        self.all = [i for i in self.all if i != plugin]
                else:
                    print(f"{plugin} устарел")
                    self.all = [i for i in self.all if i != plugin]
        return pl


def upd_id(number):
    global group_id
    global group_mention
    group_id = number
    group_mention = f'[club{group_id}|@canarybot]'


def parse_mention(mentiontoparse):
    mention = mentiontoparse.replace(mentiontoparse[mentiontoparse.find('|'):], '')

    mention = mention.replace('id', '')
    mention = mention.replace('club', '-')
    mention = mention.replace('public', '-')
        
    return int(mention)


def parse_command(messagetoreact):

    response = []
    message = messagetoreact.replace(':::CANARYBOT:mention:::', '').split()
    
    if group_mention in message:
        if message[0] == group_mention and len(message) > 1:
            message.pop(0)
            for i in message:
                if i[0] == '[' and i[-1] == ']' and i.count('|') == 1:
                    response.append(parse_mention(i[1:-1]))
                else:
                    response.append(i)
        else:
            response.append(':::CANARYBOT:mention:::')
        
    return response

class assets():
    """
    lib_assets(filename, mode): open path.
    """


    def __call__(self, filename, mode):
        return open(os.path.abspath(os.path.dirname(__file__)) + '\\assets\\' + filename, mode)


if __name__ == "__main__":
    # Подключение файла из папки lib 
    # testlib = plugins_autoimport()
    # testlib.package.check() #lib/package/main.py check()

    v = '0.01.001'

    # Подключение медиафайла из папки assets
    testassets = assets()

    test2 = open('test.jpg', "wb")
    with testassets('test.jpg', "rb") as origin:
        test2.write(origin.read())

    # Список плагинов
    testplugins = plugins(v, testassets)
    
    print(testplugins.plugins)
    print(testplugins.all)
    print(testplugins.getPlugins())
