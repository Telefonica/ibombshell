from pathlib import Path

from termcolor import colored, cprint

from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "KILL Warrior",
                       "Description": "Kill a warrior in war",
                       "Author": "@toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

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
            function = """function quit{
    global:printMessage -message "See you!"
    $global:condition = $false
}

"""
            function += 'quit'

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
