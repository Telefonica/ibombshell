import os

from termcolor import colored, cprint


class Module(object):
    def __init__(self, information, options):
        self._information = information
        self.options = options
        self.args = {}
        self.init_args()

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
