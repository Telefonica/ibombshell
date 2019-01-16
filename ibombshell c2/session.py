import importlib
import sys

from termcolor import colored, cprint


class Session(object):

    def __init__(self, path):
        self._module = None
        try:
            self._module = self.instantiate_module(self.import_path(path))
        except Exception:
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
            cprint('[!] REQUIRED ARGUMENTS NOT SET...exiting', 'red')
            return

        cprint('[+] Running module...', 'green')
        try:
            self._module.run_module()
        except KeyboardInterrupt:
            cprint('[!] Exiting the module...\n', 'red')
        except IndentationError as error:
            cprint('[!] Error running the module:\n', 'red')
            cprint("  => " + str(error), 'red')
            cprint('\n[+] Module exited\n', 'green')
        except Exception as error:
            cprint('[!] Error running the module:\n', 'red')
            cprint("  => " + str(error), 'red')
            cprint('\n[+] Module exited\n', 'green')

    def set(self, name, value):
        if name not in self._module.get_options_names():
            cprint('[!] Field not found\n', 'red')
            return
        self._module.set_value(name, value)

    def instantiate_module(self, path):
        try:
            print ('[+] Loading module...')
            m = importlib.import_module(path)
            cprint('[+] Module loaded!', 'green')
            return m.CustomModule()
        except ImportError as error:
            cprint('[!] Error importing the module:', 'red')
            cprint("  => " + str(error), 'red')
            print ("")
            return None

    def correct_module(self):
        if self._module is None:
            return False
        return True

    def import_path(self, path):
        path = path.split('/')
        path = path[path.index('modules'):]
        return ".".join(path)[:-3]

    def get_options(self):
        return ['set ' + key for key, value in self._module.get_options_dict().items()]

    def get_options_name(self):
        return list(self._module.get_options_names())