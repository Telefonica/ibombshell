from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "download-file",
                       "Description": "Download a file",
                       "Author": "@josueencinar"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "source": [None, "File source", True],
                    "destination": [None, "Destination folder", True]}}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function download-file {
                    param(
                            [Parameter(Mandatory)]
                            [string] $source,
                            [Parameter(Mandatory)]
                            [string] $destination
                        )
                        try{    
                            Start-BitsTransfer -Source $source -Destination $destination
                        } catch {
                            printMessage -message "$_.Exception.Message" 
                        }

                    }
            """

        function += 'download-file -sorce' + self.args["source"] + ' -destination ' + self.args["destination"]
        super(CustomModule, self).run(function)