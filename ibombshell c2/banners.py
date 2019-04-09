from random import choice
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

info += colored('[-*-]                  ', 'blue')
info += colored('Josué Encinar', 'red')
info += colored('(', 'blue')
info += colored('@josueencinar', 'green')
info += colored(')          [-*-]\n', 'blue')

info += colored('[-*-]                     Version: ', 'blue')
info += colored('0.0.3b', 'red')
info += colored('                    [-*-]\n', 'blue')

info += colored('[-*-]              Codename: \'', 'blue')
info += colored('The first boom...', 'yellow')
info += colored('\'             [-*-]\n', 'blue')

banner1 = """
      ,--.!,    _ ____                  __   _____ __         ____
   __/   -*-   (_) __ )____  ____ ___  / /_ / ___// /_  ___  / / /
 ,d08b.  '|`  / / __  / __ \/ __ `__ \/ __ \\\__ \/ __ \/ _ \/ / /
 0088MM      / / /_/ / /_/ / / / / / / /_/ /__/ / / / /  __/ / /
 `9MMP'     /_/_____/\____/_/ /_/ /_/_.___/____/_/ /_/\___/_/_/
"""

banner2 = """
               ██▓ ▄▄▄▄     ██████ 
               ▓██▒▓█████▄ ▒██    ▒ 
 ,!--.,        ▒██▒▒██▒ ▄██░ ▓██▄          ,--.!,
 -*-   \__     ░██░▒██░█▀    ▒   ██▒    __/   -*-
 '|`  ,b86d.   ░██░░▓█  ▀█▓▒██████▒▒  ,d87b.  '|` 
      XD8700   ░▓  ░▒▓███▀▒▒ ▒▓▒ ▒ ░  0086XD
      `PMM9'   ▒ ░▒░▒   ░ ░ ░▒  ░ ░   `9MMP'
               ▒ ░ ░    ░ ░  ░  ░  
               ░   ░            ░                                                                                                       
"""

banner3 = """
      ,-----.!,
   __/      -*-
  /         '|`
 _)  __ )                     |      ___|   |            |  | 
  |  __ \    _ \   __ `__ \   __ \ \___ \   __ \    _ \  |  | 
  |  |   |  (   |  |   |   |  |   |      |  | | |   __/  |  | 
 _| ____/  \___/  _|  _|  _| _.__/ _____/  _| |_| \___| _| _|                                                            
"""

banner4 = """
        ____    __              ___    ___      
 __    /\  _`\ /\ \            /\_ \  /\_ \     
/\_\   \ \,\L\_\ \ \___      __\//\ \ \//\ \    
\/\ \   \/_\__ \\ \  _ `\  /'__`\\ \ \  \ \ \   
 \ \ \  __/\ \L\ \ \ \ \ \/\  __/ \_\ \_ \_\ \_ 
  \ \_\/\_\ `\____\ \_\ \_\ \____\/\____\/\____/
   \/_/\/_/\/_____/\/_/\/_/\/____/\/____/\/____/
"""

banner5 = """                             
                                ██    ██      
                    ██████      ██  ██        
                  ██      ██                  
                ██          ████░░░   ████    
                ██                            
              ██████            ██  ██           
          ██████████████                      
        ██████░░░░░░░░▓▓██                    
      ██████░░░░░░░░░░▓▓▓▓██      ______   ____     ____        
      ██████▓▓▓▓▓▓▓▓░░░░▓▓██     /\__  _\ /\  _`\  /\  _`\      
     ███████▓▓▓▓▓▓▓▓▓▓░░▓▓▓██    \/_/\ \/ \ \ \L\ \\ \,\L\_\     
     ███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██       \ \ \  \ \  _ <'\/_\__ \    
     ███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██        \_\ \__\ \ \L\ \ /\ \L\ \   
      ████████▓▓▓▓▓▓▓▓▓▓▓▓██         /\_____\\ \____/ \ `\____\   
       ███████████▓▓▓▓▓▓███          \/_____/ \/___/   \/_____/   
        ████████████████                    
          ████████████                                                                                     
"""

def get_banner():
    banners = [banner1, banner2, banner3, banner4, banner5]
    return colored(choice(banners), 'yellow') + info