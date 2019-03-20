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
from subprocess import Popen, PIPE
from termcolor import cprint
import argparse
from pynput.keyboard import Controller
import threading
from time import sleep
import banners
from autocomplete import Completer
from session import Session
from warrior import Warrior
from setglobal import Global
from printib import print_ok, print_info, print_error
from help import show_help

class Console:
    def console(self):
        # commands & functions
        self.switcher = {
                    "load": self.load,
                    "set": self.set,
                    "unset": self.unset,
                    "global": self.setglobal,
                    "show": self.show,
                    "run": self.run,
                    "back": self.back,
                    "warrior": self.warrior,
                    "quit": self.quit,
                    "help": self.help,
        }
        # Configuring the commpleter
        self.comp = Completer(['load', 'set', 'unset', 'global', 'show', 'run', 'back', 'warrior', 'quit', 'help'])
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.comp.complete)

        print (banners.get_banner())
        cprint(' [+]', 'yellow', end='')
        print (' Starting the console...')
        cprint(' [*]', 'green', end='')
        print (' Console ready!\n')

        self.session = None
        
        while True:
            try:
                if self.session is None:
                    # /* Definitions available for use by readline clients. */
                    # define RL_PROMPT_START_IGNORE  '\001'
                    # define RL_PROMPT_END_IGNORE    '\002'
                    user_input = input('\001\033[1;32m\002iBombShell> \001\033[0m\002').strip()
                else:
                    user_input = input('iBombShell[' +
                                    '\001\033[1;32m\002' +
                                    self.session.header() +
                                    '\001\033[0m\002' +
                                    ']> ').strip()
                
                if user_input == "":
                    continue
                else:
                   self.switch(user_input)
            except KeyboardInterrupt:
                print("")
                Warrior.get_instance().kill_warriors()
            except Exception as e:
                print_error(e)
    # Switcher
    def switch(self, u_input):
        try:
            if u_input.startswith("#"):
                self.execute_command(u_input[1:])
            else:
                u_input = u_input.split()
                if len(u_input) >=  2:
                    self.switcher.get(u_input[0], self._command_error)(u_input[1:])
                else:
                    self.switcher.get(u_input[0], self._command_error)()
        except Exception as e:
            print_error(e)
    
    # Functions to check errors begin
    def _command_error(self):
        raise Exception('Command not found')

    def _raise_exception_specify(self, option):
        raise Exception("Specify %s" %(option))
    
    def _check_load_module(self):
        if not self.session:
            raise Exception('Please, load a module')
    
    def _check_set(self, user_input, op=2):
        self._check_load_module()
        throw  = False
        if op == 1:
            if not user_input: 
                throw  = True
        else:   
            if not (len(user_input) >= 2):
                throw  = True
        if throw:
            self._raise_exception_specify("value")
    # Functions to check errors end

    # Command functionality begin
    def execute_command(self, command):
        try:
            data = Popen(command, shell=True, stdout=PIPE).stdout.read()
            print("")
            for line in data.decode().split("\n"):
                print_info(line)
        except Exception as e:
            raise Exception(str(e))

    def load(self, user_input=None):
        if not user_input:
            self._raise_exception_specify("module")
        self.session = Session(user_input[0])               
        # The module is incorrect
        if not(self.session.correct_module()):
            print_error('Invalid module')
            self.session = None
        else:
            self.comp.set_commands_to_set(self.session.get_options_name())

    def set(self, user_input=[]):
        self._check_set(user_input)
        value = ' '.join([str(x) for x in user_input[1:]])
        self.session.set(user_input[0], value)

    def unset(self, user_input=[]):
        self._check_set(user_input, op=1)
        self.session.unset(user_input[0])

    def setglobal(self, user_input=[]):
        self._check_set(user_input)
        try:
            value = ' '.join([str(x) for x in user_input[1:]])
            self.session.set(user_input[0], value)
            Global.get_instance().add_value(user_input[0], value)
        except:
            print_error("Option not found for your configuration, use show")

    def show(self, user_input=[]):
        self._check_load_module()
        self.session.show()

    def run(self, user_input=[]):
        self._check_load_module()
        self.session.run()

    def back(self,user_input=[]):
        self.session = None

    def warrior(self, user_input=[]):
        check_len_2 = (len(user_input) >= 2)
        if  user_input[0] == 'list':
            Warrior.get_instance().print_warriors()
        elif user_input[0] == "rename":
            if not check_len_2:
                self._raise_exception_specify("warrior")
            Warrior.get_instance().rename_warrior(user_input[1])
        elif user_input[0] == "kill":
            if not check_len_2:
                self._raise_exception_specify("warrior")
            Warrior.get_instance().kill_warrior(user_input[1])

    def quit(self, user_input=[]):
        Warrior.get_instance().kill_warriors()

    def help(self, user_input=[]):
       show_help()
    # Command functionality end

def load_instructions(f):
    keyboard = Controller()
    sleep(1)
    data_file = open(f)
    for line in data_file.readlines():
        keyboard.type(line + "\n")
        sleep(0.2)

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="File with instructions for iBombShell")
    args = parser.parse_args()
    if args.file:
        th = threading.Thread(target=load_instructions, args=(args.file,))
        th.start()
    Console().console()