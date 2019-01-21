from termcolor import colored, cprint
from module import Module

class CustomModule(Module):

    def __init__(self):
        information = {"Name": "Get Processes",
                       "Description": "Check the processes running in Windows",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "name": ["", "Process name", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function gprocess {
                param(
                [Parameter(Mandatory=$false)]
                [String] $name
                )
                $admin =  [bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")
                $aux = ""

                if ($admin) {
                    $aux = " -IncludeUserName"
                }

                if ($name) {
                    $name = "*" + $name + "*"
                    $ins =  "Get-Process -Name " + $name 
                } else {
                    $ins =  "Get-Process" 
                }
                if ($isadmin) {
                    return ($ins | iex | Format-Table Id, ProcessName, UserName | out-string)
                } else {
                    return ($ins | iex | Format-Table Id, ProcessName | out-string)
                }
            }
            """

        if self.args["name"]:
            function += "gprocess -name " + self.args["name"]
        else:
            function += "gprocess"

        super(CustomModule, self).run(function)