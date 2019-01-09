from termcolor import colored, cprint
from warrior_check import exist_warrior
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
        if exist_warrior(self.args["warrior"]):
            function = """function pshell-local{
  param(
    [Parameter(Mandatory)]
    [String] $instruction
  )
  
  $instruction | iex
}

"""
            function += 'pshell-local -instruction "{}"'.format(self.args["instruction"])

            # TODO: Reemplazar la escritura por añadido (append)
            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                # f.write(routeId)
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
