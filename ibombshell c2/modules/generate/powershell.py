from termcolor import colored, cprint
from module import ModuleGenerate
from printib import print_ok, print_info, print_error
from base64 import b64encode

class CustomModule(ModuleGenerate):

    def __init__(self):
        information = {"Name": "Generate PowerShell iBombShell ",
                       "Description": "This module generates a code to launch iBombShell from powershell",
                       "Author": "@josueencinar"}
        # Constructor of the parent class
        super(CustomModule, self).__init__(information)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        ps = "powershell.exe -W Hidden {} {}"
        self.run(ps, "ps1")