import abc
import typing
from . import mention, package

class tools(abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Incorrect usage")


    @property
    @abc.abstractmethod
    def assets(self):
        pass    
        
        
    class name_cases:
        nom = 'nom'
        gen = 'gen'
        dat = 'dat'
        acc = 'acc'
        ins = 'ins'
        abl = 'abl'

    @property
    @abc.abstractmethod
    def values(self):
        pass


    @property
    @abc.abstractmethod
    def api(self):
        pass


    @property
    @abc.abstractmethod
    def http(self):
        pass


    @abc.abstractmethod
    def gen_random(self) -> int:
        """generate random number for tools.api.messages.send"""


    @abc.abstractmethod
    def log(self, *args, write: typing.Optional[str] = None, module: str = "module", level:str = "info", sep = " ") -> None:
        """
        log message
        write [str] - instead of args
        module [str] - source of message
        level [str] - log level [CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET]
        sep - args separator
        """


    @abc.abstractmethod
    def getBotId(self) -> int:
        "get community identificator [for example -1]"


    @abc.abstractmethod
    def getBotLink(self) -> str:
        "get bot address [for example \"apiclub\""


    @abc.abstractmethod
    def getBotDogMention(self) -> mention:
        """
        Get Mention as testcanarybot.objects.mention
        To get mention at format [id|string] use repr(tools.getBotDogMention())
        """

    @abc.abstractmethod
    def getBotMentions(self) -> list:
        """
        get all mentions that you set as bot mentions at commands
        """


    @abc.abstractmethod
    def wait_check(self, package) -> bool:
        "check if reply from package chat is ready"


    @abc.abstractmethod
    async def wait_reply(self, package: package) -> package:
        "wait for reply from chat from where the package is"


    @abc.abstractmethod
    async def getMention(self, page_id: int, name_case: str = "nom", name: bool = True, last_name: bool = False) -> str:
        "get mention"


    @abc.abstractmethod
    async def getManagers(self, group_id = None) -> list:
        "get managers of this group"


    @abc.abstractmethod
    async def isManager(self, from_id: int, group_id = None) -> bool:
        """
        is user is group administrator
        from_id [int] - user identificator
        group_id [int] = your bot id - group identificator
        """


    @abc.abstractmethod
    async def getChatManagers(self, peer_id: int) -> list:
        """
        get a list of managers of this chat
        peer_id [int] - chat id
        """
        

    @abc.abstractmethod
    def isChatManager(self, from_id, peer_id: int) -> bool:
        """
        is user a manager at this chat
        from_id [int] - user identificator
        peer_id [int] - chat id
        """


    @abc.abstractmethod
    async def getMembers(self, peer_id: int) -> list:
        """
        get a list of chat members
        peer_id [int] - chat id
        """


    @abc.abstractmethod
    async def isMember(self, from_id: int, peer_id: int) -> bool:
        """
        is user a chat member
        from_id [int] - user identificator
        peer_id [int] - chat id
        """