from pathlib import Path
from termcolor import cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Get default users",
                       "Description": "Lists the default users to discover which ones are enabled",
                       "Author": "@josueencinar"}

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
            function = """function get-defaultusers{
   $localEnabled = Get-LocalUser |  where-object {$_.Enabled -match "True"}
   
   $aux = "__Enabled Accounts__`r`n"
   Foreach ($u in $localEnabled){
      $aux = $aux + $u + "`r`n"
   }
   $localNotEnabled = Get-LocalUser |  where-object {$_.Enabled -match "False"}
   $aux = $aux + "`r`n__Not Enabled Accounts__`r`n"
   Foreach ($u in $localNotEnabled){
      $aux = $aux + $u + "`r`n"
   }
   return $aux
}
"""
            function += "get-defaultusers"
            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')