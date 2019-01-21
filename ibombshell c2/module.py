import os
from config import Config
from termcolor import colored, cprint
from warrior import Warrior


class Module(object):
    def __init__(self, information, options):
        self._information = information
        self.options = options
        self.args = {}
        self.init_args()
        self.warrior_path = Config.get_instance().get_warrior_path()

    def get_information(self):
        return self._information

    def set_value(self, name, value):
        self.args[name] = value
        self.options[name][0] = value

    def get_value(self, option):
        return self.args[option]

    def get_options_dict(self):
        return self.options

    def get_options_names(self):
        return self.options.keys()

    def init_args(self):
        for key, opts in self.options.items():
            self.args[key] = opts[0]

    def run_module(self):
        raise Exception(
            'ERROR: run_module method must be implemented in the child class')
    
    def run(self, function):
        if Warrior.get_instance().exist_warrior(self.args["warrior"]):
            with open('{}ibs-{}'.format(self.warrior_path, self.args["warrior"]), 'a') as f:
                # TODO: Reemplazar la escritura por añadido (append)
                f.write(function)
                cprint ('[+] Done!', 'green')
        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')


    def check_arguments(self):
        for key, value in self.options.items():
            if value[2] is True and str(value[0]) == "None":
                return False
        return True

    def print_ok(self, s):
        s = "SUCCESS: " + s
        colored(s, 'green')

    def print_ko(self, s):
        s = "ERROR: " + s
        colored(s, 'red')

    def print_warning(self, s):
        s = "WARNING: " + s
        colored(s, 'magenta')

    def print_info(self, s):
        colored(s, 'yellow')

    def run_binary(self, binary, args=None):
        payload = binary
        if args:
            payload += " " + " ".join(args)
        os.system(payload)
