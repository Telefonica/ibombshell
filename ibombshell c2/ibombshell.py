import os
try:
    import readline
    import rlcompleter
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except:
    pass
from pathlib import Path
from termcolor import colored, cprint
import banners
from autocomplete import Completer
from session import Session
from warrior import Warrior


END_COMMANDS = ['quit', 'exit', 'q']
CLEAR_COMMANDS = ['clear', 'cls']


 

def console():
    # Configuring the commpleter
    comp = Completer(['load', 'set', 'show', 'run', 'back', 'warrior', 'quit', 'help'])
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)

    print (banners.get_banner())
    cprint(' [+]', 'yellow', end='')
    print (' Starting the console...')
    cprint(' [*]', 'green', end='')
    print (' Console ready!\n')

    session = None
    
    while True:
        try:
            if session is None:
                # With termcolor not work colors
                # user_input = input(
                #     colored('iBombShell> ', 'green', attrs=['bold'])).split()

                # /* Definitions available for use by readline clients. */
                # define RL_PROMPT_START_IGNORE  '\001'
                # define RL_PROMPT_END_IGNORE    '\002'
                user_input = input('\001\033[1;32m\002iBombShell> \001\033[0m\002').split()
            else:
                # user_input = input(
                #     "iBombShell["
                #     + colored(session.header(), 'green', attrs=['bold'])
                #     + "]> ").split()

                user_input = input('iBombShell[' +
                                '\001\033[1;32m\002' +
                                session.header() +
                                '\001\033[0m\002' +
                                ']> ').split()

            if user_input == []:
                continue
            elif user_input[0] in CLEAR_COMMANDS:
                os.system('cls' if os.name=='nt' else 'clear')
            elif user_input[0] == 'back':
                session = None
            elif user_input[0] == 'warrior' and len(user_input) >= 2:
                if  user_input[1] == 'list':
                    Warrior.get_instance().print_warriors()
                elif user_input[1] == "rename":
                    if  len(user_input) > 2:
                        Warrior.get_instance().rename_warrior(user_input[2])
                    else:
                        raise Exception("Specify the warrior")
                elif user_input[1] == "kill":
                    if  len(user_input) > 2:
                        Warrior.get_instance().kill_warrior(user_input[2])
                    else:
                        raise Exception("Specify the warrior")
            elif user_input[0] in END_COMMANDS:
                Warrior.get_instance().kill_warriors()

            elif user_input[0] == 'load':
                if (len(user_input) == 1):
                    cprint('[!] Please, load a module', 'red')
                    continue
                session = Session(user_input[1])               

                # The module is incorrect
                if not(session.correct_module()):
                    cprint('[!] Invalid module', 'red')
                    session = None
                else:
                    comp.set_commands_to_set(session.get_options_name())

            elif user_input[0] == 'show':
                if session is None:
                    cprint('[!] Please, load a module', 'red')
                    continue
                session.show()

            elif user_input[0] == 'set':
                if session is None:
                    cprint('[!] Please, load a module', 'red')
                    continue
                else:
                    value = ' '.join([str(x) for x in user_input[2:]])
                    session.set(user_input[1], value)

            elif user_input[0] == 'run':
                if session is None:
                    cprint('[!] Please, load a module', 'red')
                    continue
                session.run()
            else:
                cprint('[!] Command not found', 'red')
        except KeyboardInterrupt:
            print("")
            Warrior.get_instance().kill_warriors()
        except Exception as e:
            cprint(e, "red")

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    console()

