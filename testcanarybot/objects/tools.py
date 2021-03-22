import abc
from .data import package

class tools(abc.ABCMeta):
    __module = "system"
    
    @property
    @abc.abstractmethod
    def name_cases(self):
        pass

    @property
    @abc.abstractmethod
    def mentions_self(self):
        pass

    @property
    @abc.abstractmethod
    def mentions_unknown(self):
        pass

    @property
    @abc.abstractmethod
    def values(self):
        return self.__values

    @property
    @abc.abstractmethod
    def link(self):
        pass

    @property
    @abc.abstractmethod
    def mention(self):
        pass

    @property
    @abc.abstractmethod
    def mentions(self):
        pass

    @property
    @abc.abstractmethod
    def api(self):
        pass

    @property
    @abc.abstractmethod
    def groupId(self):
        pass
        
    @property
    @abc.abstractmethod
    def http(self):
        pass
        
    @property
    @abc.abstractmethod
    def log(self):
        pass

    @property
    @abc.abstractmethod
    def random_id(self):
        pass


    @abc.abstractmethod
    def system_message(self, *args, write = None, module = None, newline = False) -> None:
        pass


    @abc.abstractmethod
    def getDate(self, time = None) -> str:
        pass
    
    
    @abc.abstractmethod
    def getTime(self, time = None) -> str:
        pass


    @abc.abstractmethod
    def getDateTime(self, time = None) -> str:
        pass
    

    @abc.abstractmethod
    def ischecktype(self, checklist, checktype) -> bool:
        pass


    @abc.abstractmethod
    def wait_check(self, package) -> bool:
        pass


    @abc.abstractmethod
    async def wait_reply(self, package: package) -> package:
        pass


    @abc.abstractmethod
    async def getMention(self, page_id: int, name_case = "nom") -> str:
        pass


    @abc.abstractmethod
    async def getManagers(self, group_id = None) -> list:
        pass


    @abc.abstractmethod
    async def isManager(self, from_id: int, group_id = None) -> bool:
        pass


    @abc.abstractmethod
    async def getChatManagers(self, peer_id: int) -> list:
        pass
        

    @abc.abstractmethod
    def isChatManager(self, from_id, peer_id: int) -> bool:
        pass


    @abc.abstractmethod
    async def getMembers(self, peer_id: int):
        pass


    @abc.abstractmethod
    async def isMember(self, from_id: int, peer_id: int) -> bool:
        pass


