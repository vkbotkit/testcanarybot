from datetime import datetime

class mentions_self:
    nom = 'я'; gen = ['меня', 'себя']; dat = ['мне', 'себе']
    acc = ['меня', 'себя']; ins = ['мной', 'собой']; abl = ['мне','себе']


class mentions_unknown:
    all = 'всех'
    him = 'его'; her = 'её'; it = 'это'
    they = 'их'; them = 'их'; us = 'нас'
    

name_cases = ['nom', 'gen', 'dat', 'acc', 'ins', 'abl']
everyone = ['@everyone', '@all', '@все']

def getDate(time = datetime.now()) -> str:
    return f'{"%02d" % time.day}.{"%02d" % time.month}.{time.year}'
    

def getTime(time = datetime.now()) -> str:
    return f'{"%02d" % time.hour}:{"%02d" % time.minute}:{"%02d" % time.second}.{time.microsecond}'


def getDateTime(time = datetime.now()) -> str:
    return self.getDate(time) + ' ' + self.getTime(time)


def ischecktype(checklist, checktype) -> bool:
    for i in checklist:
        if isinstance(checktype, list) and type(i) in checktype:
            return True
            
        elif isinstance(checktype, type) and isinstance(i, checktype): 
            return True
        
    return False
