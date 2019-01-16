from termcolor import colored, cprint
from warrior_check import exist_warrior
from module import Module
from warrior import Warrior
from time import sleep


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "KILL Warrior",
                       "Description": "Kill a warrior in war",
                       "Author": "@toolsprods, @josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        warrior = self.args["warrior"]
        if exist_warrior(warrior):
            if(Warrior.get_instance().get_status(warrior) != "Dead"):
                print("Killing warrior {}".format(warrior))
                function = """function quit{
                    $global:condition = $false
                }
                """
                function += 'quit'
                with open('/tmp/ibs-{}'.format(warrior), 'a') as f:
                    f.write(function)
                sleep(6)
            else:
                cprint ('[+] Warrior is dead', 'yellow')
            
            Warrior.get_instance().remove_warrior(warrior)
            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
