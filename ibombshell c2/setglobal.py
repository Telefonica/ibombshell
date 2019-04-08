from termcolor import colored, cprint
import sys


class Global:
    __instance = None

    @staticmethod
    def get_instance():
        if Global.__instance == None:
            Global()
        return Global.__instance

    def __init__(self):
        if Global.__instance == None:
            Global.__instance = self
            self.variables = {}
    
    def add_value(self, key, value):
        self.variables[key] = value

    def unset(self, key):
        try:
            if self.variables[key]:
                self.add_value(key, None)
        except Exception as e:
            pass
    
    def get_variables(self):
        return self.variables
    
    def show_variables(self):
        cprint(" Options (Field = Value)", 'yellow')
        print (" -----------------------")
        flag = 0
        for key, value in self.variables.items():
            flag += 1
            if flag > 1:
                print (" |")
            sys.stdout.write(" |_")
            sys.stdout.write("%s" % key)
            sys.stdout.write(" = %s \n" % (value))
        print("")