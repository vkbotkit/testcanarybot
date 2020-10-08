import msvcrt
import sys
import canarybot

# failed attempt to make canarybot with a console
# standart input() in python is blocking, but I wanted to make
# input working while canarybot takes a responses from VK  

# if you want to work with commands in canarybot, use "python -i canarybot.py"  

# so beta cmd


def getSymbol():
    sys.stdout.flush()
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'\r':
            key = '\n'
        else:
            key = key.decode()

        print(key, end='')
        sys.stdout.flush()
        
        return str(key)

inputing = ''
command = ''

print('>>> ', end='')

while True:
    symbol = getSymbol()

    if symbol:
        if symbol != '\n':
            inputing += symbol

        else:
            try:
                exec(inputing)
                print('>>> ', end='')
            except Exception as e:
                print(e)

            inputing = ''

    canarybot.check(False)