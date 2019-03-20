import os
from config import Config
from termcolor import colored, cprint
from warrior import Warrior
from setglobal import Global
from printib import print_ok, print_info, print_error

class Module(object):
    def __init__(self, information, options):
        self._information = information
        self.options = options
        self.args = {}
        self.warrior_path = Config.get_instance().get_warrior_path()
        self.update_global()
        self.update_options()
        self.init_args()
    
    def update_global(self):
        variables = Global.get_instance().get_variables()
        for key, value in self.options.items():
            try:
                if variables[key]:
                    continue
            except:
                Global.get_instance().add_value(key, None)
    
    def update_options(self):
        variables = Global.get_instance().get_variables()
        for key, value in self.options.items():
            try:
                value = variables[key]
                if value:
                    self.options[key][0] = value
            except:
                pass

    def get_information(self):
        return self._information

    def set_value(self, name, value):
        self.args[name] = value
        self.options[name][0] = value
        if value:
            msg = name + " >> " + value
            print_info(msg)

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
        if not Warrior.get_instance().exist_warrior(self.args["warrior"]):
            raise Exception('Failed... Warrior don´t found')
        with open('{}ibs-{}'.format(self.warrior_path, self.args["warrior"]), 'a') as f:
            # TODO: Reemplazar la escritura por añadido (append)
            f.write(function)
            print_ok ('Done!')

    def check_arguments(self):
        for key, value in self.options.items():
            if value[2] is True and str(value[0]) == "None":
                return False
        return True
    '''
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
    '''

    def run_binary(self, binary, args=None):
        payload = binary
        if args:
            payload += " " + " ".join(args)
        os.system(payload)
