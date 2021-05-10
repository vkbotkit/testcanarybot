import typing
from .. import exceptions

from ..enums import events as enums_events
from ..enums import action as enums_action


def ContextManager(events:typing.Optional[list]=None, commands:typing.Optional[list]=None, action:typing.Optional[list]=None,
        private:bool=False) -> None:

    def decorator(coro: typing.Callable):
        def registerCommand(self):
            if events:
                for i in events:
                    if not isinstance(i, enums_events):
                        raise TypeError("Incorrect type!")

                    elif i not in self.handlers['private']['events']['all'] and i != enums_events.message_new:
                        response = {'libraryModule': self, 'handler': coro}

                        self.handlers['private']['events']['all'].append(i)
                        self.handlers['private']['events']['coros'][i] = response

                        if not private: 
                            self.handlers['public']['events']['all'].append(i)
                            self.handlers['public']['events']['coros'][i] = response

                    else:
                        raise exceptions.LibraryRewriteError(f"\"{str(i)}\" is already registered event")
                
                return 

            if commands:
                for i in range(len(commands)):
                    if isinstance(commands[i], str):
                        commands[i] = [commands[i]] 

                response = {'libraryModule': self, 'handler': coro, 'commands': commands}
                self.handlers['private']['commands'][coro.__name__] = response
                if not private:
                    self.handlers['public']['commands'][coro.__name__] = response

                return

            if action:
                for i in action:
                    if not isinstance(i, enums_action):
                        raise TypeError("use testcanarybot.enums.action for this context!")
                    
                    if i not in self.handlers['private']['action']:
                        response = {'libraryModule': self, 'handler': coro}

                        self.handlers['private']['action'][i] = coro
                        if not private: self.handlers['public']['action'][i] = coro

                    else:
                        raise exceptions.LibraryRewriteError(f"{str(i)} is already registered action")

                return

            if not (events or commands or action):
                if 'void' in self.handlers:
                    raise NameError("Void handler is already created")

                response = {
                    'libraryModule': self,
                    'coro': coro
                }

                self.handlers['private']['void'] = response
                if not private: self.handlers['public']['void'] = response

                return
        
        return registerCommand
        
    return decorator
    
def event(events:list, private:bool=False):
    return ContextManager(events=events, private=private)


def priority(commands:list, private:bool=False):
    return ContextManager(commands=commands, private=private)


def void(coro:typing.Callable):
    return ContextManager(private=False)(coro)
    

def action(action:list, private:bool=False):
    return ContextManager(action=action, private=private)