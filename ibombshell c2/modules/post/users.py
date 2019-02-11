from termcolor import cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Local Accounts",
                       "Description": "Deal with accounts",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "option": ["list_users", "list_users / list_groups / add_user / add_user_to_group / delete_user", True],
                   "user": [None, "For add or del option", False],
                   "group": [None, "For add an user to this group", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function users{
        param(
            [Parameter(Mandatory=$true)]
            [String] $option,
            [Parameter(Mandatory=$false)]
            [String] $user,
            [Parameter(Mandatory=$false)]
            [String] $group
        )

            if ($option -eq "list_users") {
                return get-users	
            } elseif ($option -eq "add_user"){
                if(-not (isadmin)) {
                        return "There aren't enough privileges"
                    }
                    if ($user) {
                        net user $user /add	
                    } else {
                        return  "You have not written the user"
                    }
            } elseif ($option -eq "list_groups"){
                    net localgroup
            }elseif ($option -eq "add_user_to_group"){
                    if(-not (isadmin)) {
                        return "There aren't enough privileges"
                    }
                    if ($group -and $user){
                        net localgroup $group $user /add
                    }else {
                        return  "You have not written correct data... (user and group)"
                    }
            } elseif ($option -eq "delete_user") {
                    if(-not (isadmin)) {
                        return "There aren't enough privileges"
                    }
                    if ($user) {
                        net user $user /delete
                    } else {
                        return  "You have not written the user"
                    }
            } else {
                    return  "Wrong option"
            }
        }

        function get-users {

            $aux = ""
            $comp = [ADSI]"WinNT://$env:COMPUTERNAME"

            $comp.psbase.children | where { $_.psbase.schemaClassName -eq 'group' } | foreach {
                $aux = $aux + $_.name + "`r`n"
                $aux = $aux + "---------------`r`n"
                $group =[ADSI]$_.psbase.Path
                $group.psbase.Invoke("Members") | foreach {$aux = $aux + $_.GetType().InvokeMember("Name", 'GetProperty', $null, $_, $null) + "`r`n"}
                $aux = $aux + "`r`n"
                
            }

        return $aux

        }
        """
        op = self.args["option"]
        if op == "list_users" or op == "list_groups":
            function += 'users -option ' + op
        elif op == "add_user" or op == "delete_user":
            if self.args["user"]:
                function += 'users -option ' + op + ' -user ' + self.args["user"]
            else:
                cprint("Review user","red")
                return
        elif op == "add_user_to_group":
            if self.args["user"] and self.args["group"]:
                function += 'users -option ' + op + ' -user ' + self.args["user"] + " -group " + self.args["group"]
            else:
                cprint("Review user/group","red")
                return
        else:
            cprint("Wrong option...","red")
            return

        super(CustomModule, self).run(function)