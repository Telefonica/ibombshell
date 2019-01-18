from termcolor import colored, cprint
from module import Module
from warrior_check import exist_warrior


class CustomModule(Module):

    def __init__(self):
        information = {"Name": "Get Windows Apps",
                       "Description": "Check the applications installed in Windows",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)


    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = """function getapps {
                $reg = 'hkcu:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\'
                $reg2 = "hklm:SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\"
                
                $data = ''
                $data = fill-data -reg $reg
                $data =  $data + (fill-data -reg $reg2)
                
                return $data
            }

            function fill-data {
                param(
                [Parameter(Mandatory=$true)]
                [String] $reg
                )
                    $data = ''
                    try {		
                        $key = Get-Item $reg
                        if ($key) {
                            $subkeys = $key.GetSubKeyNames()
                            $key.Close()
                            foreach ($sk in $subkeys){
                                    $reg_aux = $reg + $sk
                                    $handle = Get-Item $reg_aux 
                                    $appVersion = $handle.GetValue("DisplayVersion")
                                    $appName = $handle.GetValue("DisplayName")
                                    if (!$appVersion) {
                                        $appVersion = "xxx"
                                    }
                                    if ($appName) {
                                        $data = $data + $appName+':'+ $appVersion+ '\\n'
                                    }
                                $handle.close()	    
                            }
                        }
                    } catch { }
                    return $data
            }
            """

            function += "getapps"
            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')
        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')