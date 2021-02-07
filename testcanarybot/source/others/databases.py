from . import exceptions
from . import objects

class databases:
    def __init__(self, names: list):
        self.upload(names)


    def check(self, name):
        response = [*self.__dbs.keys(), 
                *[i.directory for i in self.__dbs.values()]]

        return name in response 


    def upload(self, names):
        self.__dbs = {}
        self.add(names)


    def get(self, name):
        check = type(name)
        if check == tuple:
            if not self.check(name[0]):
                raise exceptions.DBError("This DB does not exist")

            else:
                return self.__dbs[name[1]]

        elif check == str:
            if not self.check(name):
                raise exceptions.DBError("This DB does not exist")

            else:
                return self.__dbs[name]



    def add(self, names): 
        check = type(names)

        if check == list:
            for name in names:
                if self.check(name[0]):
                    raise exceptions.DBError("This DB already exists")

                else:
                    self.__dbs[name[0]] = objects.database(name[1])

        elif check == tuple:
            if self.check(names[0]):
                raise exceptions.DBError("This DB already exists")

            else:
                self.__dbs[names[0]] = objects.database(names[1])

        elif check == str:
            if self.check(names):
                raise exceptions.DBError("This DB already exists")

            else:
                self.__dbs[names] = objects.database(names)
        
        else:
            raise exceptions.DBError("Incorrect type of 'names'")
