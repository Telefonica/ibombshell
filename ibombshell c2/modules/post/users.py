from termcolor import cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Local Accounts",
                       "Description": "Deal with accounts",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "option": ["get", "get, add or del", True],
                   "user": [None, "For add or del option", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """
        function users{
            param(
                [Parameter(Mandatory=$true)]
                [String] $option,
                [Parameter(Mandatory=$false)]
                [String] $user
            )

            if ($PSVersionTable.PSVersion.Major -lt 5) {
                return "Upgrade your powershell to version 5 or higher"
            }

                if ($option -eq "get") {
                    return get-users	
                } elseif ($option -eq "add"){
                    if ($user) {
                        New-LocalUser $user -NoPassword	
                    } else {
                        return "You have not written the user"
                    }
                } elseif ($option -eq "del") {
                    if ($user) {
                        Remove-LocalUser $user
                    } else {
                        return "You have not written the user"
                    }
                } else {
                    return  "Wrong option"
                }
        }


        function get-users {
            $localEnabled = Get-LocalUser |  where-object {$_.Enabled -match "True"}

            $aux = "__Enabled Accounts__`r`n"
            Foreach ($u in $localEnabled){
                $aux = $aux + $u + "`r`n"
            }

            $localNotEnabled = Get-LocalUser |  where-object {$_.Enabled -match "False"}

            $aux = $aux + "`r`n__Unenabled accounts__`r`n"
            Foreach ($u in $localNotEnabled){
                $aux = $aux + $u + "`r`n"
            }

            return $aux
        }
        """
        op = self.args["option"]
        if op == "get":
            function += 'users -option get'
        elif op != "add" and op != "del":
            cprint("[!] Failed... wrong option", "red")
            return
        else:
            if self.args["user"]:
                function += 'users -option ' + op + ' -user ' + self.args["user"]
            else:
                cprint("[!] Failed... User?", "red")
                return
                
        super(CustomModule, self).run(function)