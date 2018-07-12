from pathlib import Path

from termcolor import colored, cprint

from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "My own test",
                       "Description": "Test module",
                       "Author": "@toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "message1": [None, "Text description", True],
                   "message2": [None, "Text description", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):

        warrior_exist = False
        for p in Path("/tmp/").glob("ibs-*"):
            if str(p)[9:] == self.args["warrior"]:
                warrior_exist = True
                break

        if warrior_exist:
            function = """function boom{
    param(
        [string] $message,
        [string] $message2
    )
    echo $message
}

"""
            function += 'boom -message "{}"'.format(self.args["message1"])

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
