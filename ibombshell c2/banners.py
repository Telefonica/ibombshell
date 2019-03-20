import random
from termcolor import colored

# Info display
info = "\n"
info += colored('[-*-]            iBombShell - Dynamic Remote Shell           [-*-]\n', 'blue')

info += colored('[-*-]      Created by: ', 'blue')
info += colored('Pablo González', 'red')
info += colored('(', 'blue')
info += colored('@pablogonzalezpe', 'green')
info += colored(')      [-*-]\n', 'blue')

info += colored('[-*-]                  ', 'blue')
info += colored('Álvaro Núñez', 'red')
info += colored('(', 'blue')
info += colored('@toolsprods', 'green')
info += colored(')             [-*-]\n', 'blue')

info += colored('[-*-]                     Version: ', 'blue')
info += colored('0.0.3b', 'red')
info += colored('                    [-*-]\n', 'blue')

info += colored('[-*-]              Codename: \'', 'blue')
info += colored('The first boom...', 'yellow')
info += colored('\'             [-*-]\n', 'blue')

banner = """
      ,--.!,    _ ____                  __   _____ __         ____
   __/   -*-   (_) __ )____  ____ ___  / /_ / ___// /_  ___  / / /
 ,d08b.  '|`  / / __  / __ \/ __ `__ \/ __ \\\__ \/ __ \/ _ \/ / /
 0088MM      / / /_/ / /_/ / / / / / / /_/ /__/ / / / /  __/ / /
 `9MMP'     /_/_____/\____/_/ /_/ /_/_.___/____/_/ /_/\___/_/_/
"""


def get_banner():
    return colored(banner, 'yellow') + info
