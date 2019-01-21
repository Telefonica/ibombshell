from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "OS X Text to Speech Utility",
                       "Description": "This module will speak whatever is in the 'TEXT' option on the victim machine.",
                       "Author": "@toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "message": [None, "Text to say", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function say{
    param(
        [string] $message
    )
    say $message
}

"""
        function += 'say -message "{}"'.format(self.args["message"])

        super(CustomModule, self).run(function))
