from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Get Dlls",
                       "Description": "Obtain the system DLLs, according to the architecture",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):

        function = """function get-dll {
                $ErrorActionPreference = "SilentlyContinue"
                $architecture = "x86"
                if ($architecture -eq "x64") {
                    $folder = "C:\\Windows\\System32"
                }else {
                    $folder = "C:\\Windows\\SysWOW64"
                    # WinSxS 
                }
                $items = Get-ChildItem -Path $folder -Directory
                $data = ""

                foreach($item in $items) {
                    $childItems = Get-ChildItem -Path ($folder + "\\" + $item.Name) -File
                    foreach($i in $childItems){
                        if (($i.Name).endswith(".dll")){
                            $data = $data + ($folder + "\\" + $item.Name + "\\" + $i.Name) + "`n"
                        }
                    }
                }

                return $data
            }
            """
        function += "get-dll"
        super(CustomModule, self).run(function)      