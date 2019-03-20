import importlib
import sys
from os import sep
from termcolor import colored, cprint
from printib import print_ok, print_info, print_error

class Session(object):

    def __init__(self, path):
        self._module = None
        try:
            self._module = self.instantiate_module(self.import_path(path))
        except Exception as e:
            pass

        self._path = path

    def header(self):
        return self._path.split("\\")[-1]

    def show(self):
        self.information()
        self.options()

    def information(self):
        info = self._module.get_information()
        print ("")
        for key, value in info.items():
            cprint(" %s" % key, 'yellow')
            print (' ' + '-' * len(key))
            print (" |_%s\n" % value)

    def options(self):
        opts = self._module.get_options_dict()
        cprint(" Options (Field = Value)", 'yellow')
        print (" -----------------------")
        flag = 0
        for key, value in opts.items():
            flag += 1
            # Parameter is mandataroy
            if value[2] is True:
                if str(value[0]) == "None":
                    if flag > 1:
                        print (" |")
                    sys.stdout.write(" |_[")
                    cprint("REQUIRED", 'red', end='')
                    sys.stdout.write("] %s" % key)
                    sys.stdout.write(" = %s (%s)\n" % (value[0], value[1]))
                else:
                    if flag > 1:
                        print (" |")
                    sys.stdout.write(" |_%s" % key)
                    sys.stdout.write(" = ")
                    cprint("%s" % value[0], 'green', end='')
                    sys.stdout.write(" (% s)\n" % (value[1]))

            # Parameter is optional
            elif value[2] is False:
                if str(value[0]) == "None":
                    if flag > 1:
                        print (" |")
                    print (" |_[OPTIONAL] %s" % key \
                        + " = %s (%s)" % (value[0], value[1]))
                else:
                    if flag > 1:
                        print (" |")
                    sys.stdout.write(" |_%s" % key)
                    sys.stdout.write(" = ")
                    cprint("%s" % value[0], 'green', end='')
                    sys.stdout.write(" (% s)\n" % (value[1]))

        print ("\n")

    def run(self):
        if not(self._module.check_arguments()):
            raise Exception('REQUIRED ARGUMENTS NOT SET...exiting')

        print_ok('Running module...')
        try:
            self._module.run_module()
        except KeyboardInterrupt:
            print_error('Exiting the module...' )
        except Exception as error:
            m = 'Error running the module: ' + str(error)
            print_error(m)
            print_ok('Module exited')

    def set(self, name, value):
        if name not in self._module.get_options_names():
            raise Exception('Field not found')
        self._module.set_value(name, value)
    
    def unset(self, name):
        if name not in self._module.get_options_names():
            raise Exception('Field not found')
        self._module.set_value(name, None)

    def instantiate_module(self, path):
        try:
            print_ok('Loading module...')
            m = importlib.import_module(path)
            print_ok('Module loaded!')
            return m.CustomModule()
        except ImportError as error:
            m = 'Error importing the module: ' + str(error)
            print_error(m)
            return None

    def correct_module(self):
        if self._module is None:
            return False
        return True

    def import_path(self, path):
        path = path.replace(sep,".")
        return path.replace(".py","")

    def get_options(self):
        return ['set ' + key for key, value in self._module.get_options_dict().items()]

    def get_options_name(self):
        return list(self._module.get_options_names())