from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "PShell local (scope)",
                       "Description": "Execute powershell instruction in the same scope that ibombshell",
                       "Author": "@pablogonzalezpe, @toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "instruction": [None, "Instruction to execute", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):

        function = """function pshell-local{
            param(
                [Parameter(Mandatory)]
                [String] $instruction
            )
            
            $instruction | iex
            }

            """
        function += 'pshell-local -instruction "{}"'.format(self.args["instruction"])
        super(CustomModule, self).run(function)

        
           
